using System.Globalization;
using System.Net;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using System.Xml.Linq;
using CVIS.Playwright.Reporting.Models;

namespace CVIS.Playwright.Reporting;

public sealed class NUnitResultReportBuilder
{
    public CvisTestReportSummary Build(CvisReportBuildOptions options)
    {
        var entries = new List<CvisTestReportEntry>();

        var trxRoot = new DirectoryInfo(options.TrxRoot);
        if (trxRoot.Exists)
        {
            entries.AddRange(ReadTrxFiles(trxRoot));
        }

        var nunitXmlRoot = new DirectoryInfo(options.NUnitXmlRoot);
        if (nunitXmlRoot.Exists)
        {
            entries.AddRange(ReadNUnitXmlFiles(nunitXmlRoot));
        }

        var tests = Deduplicate(entries)
            .OrderBy(item => item.FullName, StringComparer.OrdinalIgnoreCase)
            .ToList();

        if (tests.Count < options.MinimumTotal)
        {
            throw new InvalidOperationException(
                $"Authoritative report found only {tests.Count} tests. Expected at least {options.MinimumTotal}. " +
                $"TRX root: {options.TrxRoot}; NUnit XML root: {options.NUnitXmlRoot}");
        }

        var summary = new CvisTestReportSummary
        {
            Framework = options.FrameworkName,
            Source = "TRX+NUnitXml",
            GeneratedUtc = DateTimeOffset.UtcNow,
            Total = tests.Count,
            Passed = tests.Count(item => item.Status == CvisTestReportStatus.Passed),
            Failed = tests.Count(item => item.Status == CvisTestReportStatus.Failed),
            Skipped = tests.Count(item => item.Status == CvisTestReportStatus.Skipped),
            Other = tests.Count(item =>
                item.Status != CvisTestReportStatus.Passed &&
                item.Status != CvisTestReportStatus.Failed &&
                item.Status != CvisTestReportStatus.Skipped),
            Tests = tests
        };

        WriteReport(summary, new DirectoryInfo(options.OutputRoot));
        return summary;
    }

    private static IReadOnlyList<CvisTestReportEntry> Deduplicate(IEnumerable<CvisTestReportEntry> entries)
    {
        var result = new Dictionary<string, CvisTestReportEntry>(StringComparer.OrdinalIgnoreCase);

        foreach (var entry in entries.OrderBy(item => item.Source == "TRX" ? 0 : 1))
        {
            result.TryAdd(entry.FullName, entry);
        }

        return result.Values.ToList();
    }

    private static IEnumerable<CvisTestReportEntry> ReadTrxFiles(DirectoryInfo root)
    {
        foreach (var file in root.EnumerateFiles("*.trx", SearchOption.AllDirectories))
        {
            XDocument document;

            try
            {
                document = XDocument.Load(file.FullName);
            }
            catch
            {
                continue;
            }

            var ns = document.Root?.Name.Namespace ?? XNamespace.None;

            var definitions = document
                .Descendants(ns + "UnitTest")
                .Select(test =>
                {
                    var testMethod = test.Descendants(ns + "TestMethod").FirstOrDefault();
                    var id = (string?)test.Attribute("id") ?? string.Empty;
                    var methodName = (string?)testMethod?.Attribute("name")
                        ?? (string?)test.Attribute("name")
                        ?? string.Empty;
                    var className = (string?)testMethod?.Attribute("className") ?? string.Empty;
                    var fullName = string.IsNullOrWhiteSpace(className)
                        ? methodName
                        : $"{className}.{methodName}";

                    return new
                    {
                        Id = id,
                        MethodName = methodName,
                        FullName = fullName
                    };
                })
                .Where(item => !string.IsNullOrWhiteSpace(item.Id))
                .ToDictionary(item => item.Id, item => item, StringComparer.OrdinalIgnoreCase);

            foreach (var result in document.Descendants(ns + "UnitTestResult"))
            {
                var testId = (string?)result.Attribute("testId") ?? string.Empty;
                definitions.TryGetValue(testId, out var definition);

                var fullName = definition?.FullName
                    ?? (string?)result.Attribute("testName")
                    ?? testId
                    ?? "Unknown";

                var testName = definition?.MethodName
                    ?? (string?)result.Attribute("testName")
                    ?? fullName;

                yield return new CvisTestReportEntry
                {
                    Id = StableId($"trx:{file.FullName}:{fullName}"),
                    TestName = testName,
                    FullName = fullName,
                    FixtureName = FixtureName(fullName),
                    Status = MapTrxOutcome((string?)result.Attribute("outcome")),
                    DurationMilliseconds = ParseTrxDuration((string?)result.Attribute("duration")),
                    Message = NullIfWhiteSpace(result.Descendants(ns + "Message").FirstOrDefault()?.Value),
                    StackTrace = NullIfWhiteSpace(result.Descendants(ns + "StackTrace").FirstOrDefault()?.Value),
                    Categories = Array.Empty<string>(),
                    Source = "TRX",
                    SourceFile = file.FullName
                };
            }
        }
    }

    private static IEnumerable<CvisTestReportEntry> ReadNUnitXmlFiles(DirectoryInfo root)
    {
        foreach (var file in root.EnumerateFiles("*.xml", SearchOption.AllDirectories))
        {
            XDocument document;

            try
            {
                document = XDocument.Load(file.FullName);
            }
            catch
            {
                continue;
            }

            foreach (var testCase in document.Descendants("test-case"))
            {
                var fullName = (string?)testCase.Attribute("fullname")
                    ?? (string?)testCase.Attribute("name")
                    ?? "Unknown";

                var testName = (string?)testCase.Attribute("name") ?? fullName;
                var failure = testCase.Element("failure");
                var reason = testCase.Element("reason");

                var categories = testCase
                    .Element("properties")
                    ?.Elements("property")
                    .Where(item => (string?)item.Attribute("name") == "Category")
                    .Select(item => (string?)item.Attribute("value"))
                    .Where(item => !string.IsNullOrWhiteSpace(item))
                    .Select(item => item!)
                    .Distinct(StringComparer.OrdinalIgnoreCase)
                    .OrderBy(item => item, StringComparer.OrdinalIgnoreCase)
                    .ToList()
                    ?? new List<string>();

                yield return new CvisTestReportEntry
                {
                    Id = StableId($"nunit:{file.FullName}:{fullName}"),
                    TestName = testName,
                    FullName = fullName,
                    FixtureName = FixtureName(fullName),
                    Status = MapNUnitOutcome((string?)testCase.Attribute("result"), (string?)testCase.Attribute("label")),
                    DurationMilliseconds = ParseSecondsToMilliseconds((string?)testCase.Attribute("duration")),
                    Message = NullIfWhiteSpace(failure?.Element("message")?.Value ?? reason?.Element("message")?.Value),
                    StackTrace = NullIfWhiteSpace(failure?.Element("stack-trace")?.Value),
                    Categories = categories,
                    Source = "NUnitXml",
                    SourceFile = file.FullName
                };
            }
        }
    }

    private static void WriteReport(CvisTestReportSummary summary, DirectoryInfo outputRoot)
    {
        outputRoot.Create();

        var testsRoot = new DirectoryInfo(Path.Combine(outputRoot.FullName, "Tests"));
        testsRoot.Create();

        var jsonOptions = new JsonSerializerOptions
        {
            WriteIndented = true
        };

        File.WriteAllText(
            Path.Combine(outputRoot.FullName, "cpn-report.json"),
            JsonSerializer.Serialize(summary, jsonOptions),
            Encoding.UTF8);

        File.WriteAllText(
            Path.Combine(outputRoot.FullName, "cpn-report-all-tests.json"),
            JsonSerializer.Serialize(summary, jsonOptions),
            Encoding.UTF8);

        foreach (var test in summary.Tests)
        {
            File.WriteAllText(
                Path.Combine(testsRoot.FullName, $"{SanitizeFileName(test.FullName)}.json"),
                JsonSerializer.Serialize(test, jsonOptions),
                Encoding.UTF8);
        }

        var html = BuildHtml(summary);

        File.WriteAllText(Path.Combine(outputRoot.FullName, "cpn-report.html"), html, Encoding.UTF8);
        File.WriteAllText(Path.Combine(outputRoot.FullName, "cpn-report-all-tests.html"), html, Encoding.UTF8);

        File.WriteAllText(
            Path.Combine(outputRoot.FullName, "cpn-report-summary.txt"),
            $"Framework: {summary.Framework}{Environment.NewLine}" +
            $"Source: {summary.Source}{Environment.NewLine}" +
            $"Total: {summary.Total}{Environment.NewLine}" +
            $"Passed: {summary.Passed}{Environment.NewLine}" +
            $"Failed: {summary.Failed}{Environment.NewLine}" +
            $"Skipped: {summary.Skipped}{Environment.NewLine}" +
            $"Other: {summary.Other}{Environment.NewLine}",
            Encoding.UTF8);
    }

    private static string BuildHtml(CvisTestReportSummary summary)
    {
        var rows = new StringBuilder();

        foreach (var test in summary.Tests.OrderBy(item => item.Status).ThenBy(item => item.FullName, StringComparer.OrdinalIgnoreCase))
        {
            var message = WebUtility.HtmlEncode(test.Message ?? string.Empty);

            if (!string.IsNullOrWhiteSpace(test.StackTrace))
            {
                message += "<details><summary>Stack trace</summary><pre>" +
                           WebUtility.HtmlEncode(test.StackTrace) +
                           "</pre></details>";
            }

            rows.AppendLine("<tr>");
            rows.Append("<td class=\"").Append(test.Status).Append("\">")
                .Append(WebUtility.HtmlEncode(test.Status.ToString()))
                .AppendLine("</td>");
            rows.Append("<td><code>").Append(WebUtility.HtmlEncode(test.FullName)).AppendLine("</code></td>");
            rows.Append("<td>").Append(WebUtility.HtmlEncode($"{test.DurationMilliseconds:N2} ms")).AppendLine("</td>");
            rows.Append("<td>").Append(WebUtility.HtmlEncode(test.Source)).AppendLine("</td>");
            rows.Append("<td>").Append(message).AppendLine("</td>");
            rows.AppendLine("</tr>");
        }

        return $$"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>CVIS Authoritative Test Report</title>
<style>
body{font-family:Segoe UI,Arial,sans-serif;margin:24px;background:#f7f7f8;color:#1f2328;}
h1{margin-bottom:4px;}
.meta{color:#57606a;margin-bottom:18px;}
.cards{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:24px;}
.card{background:white;border:1px solid #d0d7de;border-radius:8px;padding:14px 22px;min-width:120px;}
.number{font-size:30px;font-weight:700;}
table{width:100%;border-collapse:collapse;background:white;border:1px solid #d0d7de;}
th,td{text-align:left;border-bottom:1px solid #d8dee4;padding:10px;vertical-align:top;}
th{background:#f1f3f5;}
.Passed{color:#1a7f37;font-weight:700;}
.Failed{color:#cf222e;font-weight:700;}
.Skipped,.Inconclusive,.Warning,.Unknown{color:#9a6700;font-weight:700;}
code{font-family:Consolas,monospace;font-size:12px;}
pre{white-space:pre-wrap;}
</style>
</head>
<body>
<h1>CVIS Authoritative Test Report</h1>
<div class="meta">Framework: {{WebUtility.HtmlEncode(summary.Framework)}} | Source: {{WebUtility.HtmlEncode(summary.Source)}} | Generated UTC: {{WebUtility.HtmlEncode(summary.GeneratedUtc.ToString("O"))}}</div>
<div class="cards">
  <div class="card"><div class="number">{{summary.Total}}</div><div>Total</div></div>
  <div class="card"><div class="number">{{summary.Passed}}</div><div>Passed</div></div>
  <div class="card"><div class="number">{{summary.Failed}}</div><div>Failed</div></div>
  <div class="card"><div class="number">{{summary.Skipped}}</div><div>Skipped</div></div>
  <div class="card"><div class="number">{{summary.Other}}</div><div>Other</div></div>
</div>
<table>
<thead><tr><th>Status</th><th>Test</th><th>Duration</th><th>Source</th><th>Message</th></tr></thead>
<tbody>
{{rows}}
</tbody>
</table>
</body>
</html>
""";
    }

    private static CvisTestReportStatus MapTrxOutcome(string? outcome)
    {
        return outcome switch
        {
            "Passed" => CvisTestReportStatus.Passed,
            "Failed" => CvisTestReportStatus.Failed,
            "NotExecuted" => CvisTestReportStatus.Skipped,
            "Timeout" => CvisTestReportStatus.Failed,
            "Aborted" => CvisTestReportStatus.Failed,
            "Error" => CvisTestReportStatus.Failed,
            "Inconclusive" => CvisTestReportStatus.Inconclusive,
            _ => CvisTestReportStatus.Unknown
        };
    }

    private static CvisTestReportStatus MapNUnitOutcome(string? result, string? label)
    {
        return result switch
        {
            "Passed" => CvisTestReportStatus.Passed,
            "Failed" => CvisTestReportStatus.Failed,
            "Skipped" => CvisTestReportStatus.Skipped,
            "Inconclusive" => CvisTestReportStatus.Inconclusive,
            "Warning" => CvisTestReportStatus.Warning,
            _ when !string.IsNullOrWhiteSpace(label) &&
                   (label.Contains("Skipped", StringComparison.OrdinalIgnoreCase) ||
                    label.Contains("Ignored", StringComparison.OrdinalIgnoreCase)) => CvisTestReportStatus.Skipped,
            _ => CvisTestReportStatus.Unknown
        };
    }

    private static double ParseTrxDuration(string? value)
    {
        return TimeSpan.TryParse(value, CultureInfo.InvariantCulture, out var parsed)
            ? Math.Round(parsed.TotalMilliseconds, 2)
            : 0;
    }

    private static double ParseSecondsToMilliseconds(string? value)
    {
        return double.TryParse(value, NumberStyles.Float, CultureInfo.InvariantCulture, out var seconds)
            ? Math.Round(seconds * 1000, 2)
            : 0;
    }

    private static string FixtureName(string fullName)
    {
        var index = fullName.LastIndexOf('.');
        return index <= 0 ? fullName : fullName[..index];
    }

    private static string? NullIfWhiteSpace(string? value)
    {
        return string.IsNullOrWhiteSpace(value) ? null : value;
    }

    private static string StableId(string value)
    {
        var hash = SHA256.HashData(Encoding.UTF8.GetBytes(value));
        return Convert.ToHexString(hash)[..16].ToLowerInvariant();
    }

    private static string SanitizeFileName(string value)
    {
        var invalid = Path.GetInvalidFileNameChars().ToHashSet();
        var builder = new StringBuilder(value.Length);

        foreach (var character in value)
        {
            builder.Append(invalid.Contains(character) ? '_' : character);
        }

        var sanitized = builder.ToString();
        return sanitized.Length <= 150 ? sanitized : sanitized[..150];
    }
}
