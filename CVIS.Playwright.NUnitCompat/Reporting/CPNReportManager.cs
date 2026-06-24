using System.Collections.Concurrent;
using System.Net;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using NUnit.Framework;
using NUnit.Framework.Interfaces;
using CVIS.Playwright.NUnitCompat;

namespace CVIS.Playwright.NUnitCompat.Reporting;

public static class CPNReportManager
{
    private static readonly object Sync = new();
    private static readonly ConcurrentDictionary<string, CPNReportEntry> Entries = new();
    private static CPNReportOptions _options = CPNReportOptions.FromEnvironment();

    public static string ReportRoot => _options.ReportRoot;
    public static string JsonReportPath => Path.Combine(_options.ReportRoot, _options.JsonFileName);
    public static string HtmlReportPath => Path.Combine(_options.ReportRoot, _options.HtmlFileName);
    public static string TestEntriesPath => Path.Combine(_options.ReportRoot, "Tests");

    public static void Initialize()
    {
        _options = CPNReportOptions.FromEnvironment();

        if (!_options.Enabled)
        {
            return;
        }

        Directory.CreateDirectory(_options.ReportRoot);
        Directory.CreateDirectory(TestEntriesPath);
    }

    public static void RecordCurrentTest(TestContext context, DateTimeOffset startedUtc)
    {
        if (!_options.Enabled)
        {
            return;
        }

        var finishedUtc = DateTimeOffset.UtcNow;
        var fullName = context.Test.FullName;
        var result = context.Result;

        Record(new CPNReportEntry
        {
            Id = CreateStableId(fullName),
            TestName = context.Test.Name,
            FullName = fullName,
            FixtureName = ResolveFixtureName(fullName),
            Status = MapStatus(result.Outcome.Status),
            StartedUtc = startedUtc,
            FinishedUtc = finishedUtc,
            DurationMilliseconds = Math.Max(0, (finishedUtc - startedUtc).TotalMilliseconds),
            Message = NullIfEmpty(result.Message),
            StackTrace = NullIfEmpty(result.StackTrace),
            WorkerId = Environment.GetEnvironmentVariable("NUNIT_WORKER_ID")
                ?? Environment.GetEnvironmentVariable("TEST_WORKER_INDEX")
                ?? "0",
            BrowserName = Environment.GetEnvironmentVariable("BROWSER") ?? "chromium",
            Categories = Array.Empty<string>(),
            OutputLines = Array.Empty<string>(),
            Attachments = Array.Empty<string>()
        });
    }

    public static void Record(CPNReportEntry entry)
    {
        Initialize();

        if (!_options.Enabled)
        {
            return;
        }

        Entries[entry.Id] = entry;

        lock (Sync)
        {
            WriteSingleTestEntry(entry);
            WriteJsonSummary();
            WriteHtmlSummary();
        }
    }

    public static CPNReportSummary CreateSummary()
    {
        var tests = Entries.Values
            .OrderBy(item => item.StartedUtc)
            .ThenBy(item => item.FullName, StringComparer.OrdinalIgnoreCase)
            .ToList();

        return new CPNReportSummary
        {
            Framework = "CVIS.Playwright.NUnitCompat",
            GeneratedUtc = DateTimeOffset.UtcNow,
            Total = tests.Count,
            Passed = tests.Count(item => item.Status == CPNReportStatus.Passed),
            Failed = tests.Count(item => item.Status == CPNReportStatus.Failed),
            Skipped = tests.Count(item => item.Status == CPNReportStatus.Skipped),
            Inconclusive = tests.Count(item => item.Status == CPNReportStatus.Inconclusive),
            Warning = tests.Count(item => item.Status == CPNReportStatus.Warning),
            Unknown = tests.Count(item => item.Status == CPNReportStatus.Unknown),
            Tests = tests
        };
    }

    public static void ResetForTesting(string? reportRoot = null)
    {
        Entries.Clear();

        if (!string.IsNullOrWhiteSpace(reportRoot))
        {
            Environment.SetEnvironmentVariable("CPN_REPORT_ROOT", reportRoot);
        }

        _options = CPNReportOptions.FromEnvironment();

        if (Directory.Exists(_options.ReportRoot))
        {
            Directory.Delete(_options.ReportRoot, recursive: true);
        }
    }

    private static void WriteSingleTestEntry(CPNReportEntry entry)
    {
        Directory.CreateDirectory(TestEntriesPath);
        var path = Path.Combine(TestEntriesPath, SanitizeFileName(entry.FullName) + ".json");
        File.WriteAllText(path, JsonSerializer.Serialize(entry, JsonOptions()), Encoding.UTF8);
    }

    private static void WriteJsonSummary()
    {
        Directory.CreateDirectory(_options.ReportRoot);
        File.WriteAllText(JsonReportPath, JsonSerializer.Serialize(CreateSummary(), JsonOptions()), Encoding.UTF8);
    }

    private static void WriteHtmlSummary()
    {
        Directory.CreateDirectory(_options.ReportRoot);
        File.WriteAllText(HtmlReportPath, BuildHtml(CreateSummary()), Encoding.UTF8);
    }

    private static string BuildHtml(CPNReportSummary summary)
    {
        var builder = new StringBuilder();
        builder.AppendLine("<!doctype html>");
        builder.AppendLine("<html lang=\"en\"><head><meta charset=\"utf-8\" />");
        builder.AppendLine("<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />");
        builder.AppendLine("<title>CPN Test Report</title>");
        builder.AppendLine("<style>");
        builder.AppendLine("body{font-family:Segoe UI,Arial,sans-serif;margin:24px;background:#f7f7f8;color:#1f2328;}");
        builder.AppendLine(".cards{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:24px;}");
        builder.AppendLine(".card{background:white;border:1px solid #d0d7de;border-radius:8px;padding:14px 18px;min-width:110px;}");
        builder.AppendLine(".number{font-size:28px;font-weight:700;}");
        builder.AppendLine("table{width:100%;border-collapse:collapse;background:white;border:1px solid #d0d7de;}");
        builder.AppendLine("th,td{text-align:left;border-bottom:1px solid #d8dee4;padding:10px;vertical-align:top;}");
        builder.AppendLine("th{background:#f1f3f5;}.Passed{color:#1a7f37;font-weight:700;}.Failed{color:#cf222e;font-weight:700;}");
        builder.AppendLine(".Skipped,.Inconclusive,.Warning,.Unknown{color:#9a6700;font-weight:700;}code{font-family:Consolas,monospace;font-size:12px;}");
        builder.AppendLine("</style></head><body>");
        builder.AppendLine("<h1>CPN Test Report</h1>");
        builder.Append("<div>Framework: ").Append(Html(summary.Framework)).Append(" | Generated UTC: ").Append(Html(summary.GeneratedUtc.ToString("O"))).AppendLine("</div>");
        builder.AppendLine("<div class=\"cards\">");
        AddCard(builder, "Total", summary.Total);
        AddCard(builder, "Passed", summary.Passed);
        AddCard(builder, "Failed", summary.Failed);
        AddCard(builder, "Skipped", summary.Skipped);
        AddCard(builder, "Other", summary.Inconclusive + summary.Warning + summary.Unknown);
        builder.AppendLine("</div><table><thead><tr><th>Status</th><th>Test</th><th>Duration</th><th>Message</th></tr></thead><tbody>");

        foreach (var test in summary.Tests)
        {
            builder.Append("<tr><td class=\"").Append(test.Status).Append("\">").Append(Html(test.Status.ToString())).Append("</td>");
            builder.Append("<td><code>").Append(Html(test.FullName)).Append("</code></td>");
            builder.Append("<td>").Append(Html($"{test.DurationMilliseconds:N0} ms")).Append("</td>");
            builder.Append("<td>").Append(Html(test.Message ?? string.Empty)).AppendLine("</td></tr>");
        }

        builder.AppendLine("</tbody></table></body></html>");
        return builder.ToString();
    }

    private static void AddCard(StringBuilder builder, string label, int value)
    {
        builder.Append("<div class=\"card\"><div class=\"number\">").Append(value).Append("</div><div>").Append(Html(label)).AppendLine("</div></div>");
    }

    private static JsonSerializerOptions JsonOptions() => new() { WriteIndented = true };

    private static CPNReportStatus MapStatus(TestStatus status) => status switch
    {
        TestStatus.Passed => CPNReportStatus.Passed,
        TestStatus.Failed => CPNReportStatus.Failed,
        TestStatus.Skipped => CPNReportStatus.Skipped,
        TestStatus.Inconclusive => CPNReportStatus.Inconclusive,
        TestStatus.Warning => CPNReportStatus.Warning,
        _ => CPNReportStatus.Unknown
    };

    private static string ResolveFixtureName(string fullName)
    {
        var lastDot = fullName.LastIndexOf('.');
        return lastDot <= 0 ? fullName : fullName[..lastDot];
    }

    private static string? NullIfEmpty(string? value) => string.IsNullOrWhiteSpace(value) ? null : value;

private static string CreateStableId(string value)
    {
        var bytes = SHA256.HashData(Encoding.UTF8.GetBytes(value));
        return Convert.ToHexString(bytes)[..16].ToLowerInvariant();
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

    private static string Html(string value) => WebUtility.HtmlEncode(value);
}
