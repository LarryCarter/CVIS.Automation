r'''
Adds CPN report output: JSON + HTML + per-test JSON.
Run from solution root.
'''
from pathlib import Path
import textwrap

ROOT = Path.cwd()
CPN = ROOT / "CVIS.Playwright.NUnitCompat"
CPNT = ROOT / "CVIS.Playwright.NUnitCompat.Tests"

def w(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text).lstrip(), encoding="utf-8")

def main():
    if not CPN.exists():
        raise RuntimeError("Missing CVIS.Playwright.NUnitCompat")
    if not CPNT.exists():
        raise RuntimeError("Missing CVIS.Playwright.NUnitCompat.Tests")

    w(CPN / "CVISWorkerAwareTest.cs", '''
        using NUnit.Framework;
        using NUnit.Framework.Interfaces;

        namespace CVIS.Playwright.NUnitCompat;

        public abstract class CVISWorkerAwareTest
        {
            private DateTimeOffset _cpnReportStartUtc;

            protected bool TestOk()
            {
                return TestContext.CurrentContext.Result.Outcome.Status == TestStatus.Passed;
            }

            protected string TestName => TestContext.CurrentContext.Test.Name;

            protected string WorkerId =>
                Environment.GetEnvironmentVariable("NUNIT_WORKER_ID")
                ?? Environment.GetEnvironmentVariable("TEST_WORKER_INDEX")
                ?? "0";

            [SetUp]
            public void CVISWorkerAwareReportSetup()
            {
                _cpnReportStartUtc = DateTimeOffset.UtcNow;
                CPNReportManager.Initialize();
            }

            [TearDown]
            public void CVISWorkerAwareReportTearDown()
            {
                CPNReportManager.RecordCurrentTest(TestContext.CurrentContext, _cpnReportStartUtc);
            }
        }
    ''')

    w(CPN / "Reporting" / "CPNReportStatus.cs", '''
        namespace CVIS.Playwright.NUnitCompat.Reporting;

        public enum CPNReportStatus
        {
            Passed,
            Failed,
            Skipped,
            Inconclusive,
            Warning,
            Unknown
        }
    ''')

    w(CPN / "Reporting" / "CPNReportEntry.cs", '''
        namespace CVIS.Playwright.NUnitCompat.Reporting;

        public sealed record CPNReportEntry
        {
            public required string Id { get; init; }
            public required string TestName { get; init; }
            public required string FullName { get; init; }
            public required string FixtureName { get; init; }
            public required CPNReportStatus Status { get; init; }
            public required DateTimeOffset StartedUtc { get; init; }
            public required DateTimeOffset FinishedUtc { get; init; }
            public required double DurationMilliseconds { get; init; }
            public string? Message { get; init; }
            public string? StackTrace { get; init; }
            public string? WorkerId { get; init; }
            public string? BrowserName { get; init; }
            public IReadOnlyList<string> Categories { get; init; } = Array.Empty<string>();
            public IReadOnlyList<string> OutputLines { get; init; } = Array.Empty<string>();
            public IReadOnlyList<string> Attachments { get; init; } = Array.Empty<string>();
        }
    ''')

    w(CPN / "Reporting" / "CPNReportSummary.cs", '''
        namespace CVIS.Playwright.NUnitCompat.Reporting;

        public sealed record CPNReportSummary
        {
            public required string Framework { get; init; }
            public required DateTimeOffset GeneratedUtc { get; init; }
            public required int Total { get; init; }
            public required int Passed { get; init; }
            public required int Failed { get; init; }
            public required int Skipped { get; init; }
            public required int Inconclusive { get; init; }
            public required int Warning { get; init; }
            public required int Unknown { get; init; }
            public required IReadOnlyList<CPNReportEntry> Tests { get; init; }
        }
    ''')

    w(CPN / "Reporting" / "CPNReportOptions.cs", '''
        namespace CVIS.Playwright.NUnitCompat.Reporting;

        public sealed record CPNReportOptions
        {
            public bool Enabled { get; init; } = true;
            public string ReportRoot { get; init; } = string.Empty;
            public string JsonFileName { get; init; } = "cpn-report.json";
            public string HtmlFileName { get; init; } = "cpn-report.html";

            public static CPNReportOptions FromEnvironment()
            {
                var enabledValue = Environment.GetEnvironmentVariable("CPN_REPORT_ENABLED");
                var enabled = string.IsNullOrWhiteSpace(enabledValue)
                    || enabledValue.Equals("1", StringComparison.OrdinalIgnoreCase)
                    || enabledValue.Equals("true", StringComparison.OrdinalIgnoreCase)
                    || enabledValue.Equals("yes", StringComparison.OrdinalIgnoreCase);

                var reportRoot = Environment.GetEnvironmentVariable("CPN_REPORT_ROOT");
                if (string.IsNullOrWhiteSpace(reportRoot))
                {
                    reportRoot = Path.Combine(Directory.GetCurrentDirectory(), "TestResults", "CPN");
                }

                return new CPNReportOptions
                {
                    Enabled = enabled,
                    ReportRoot = reportRoot
                };
            }
        }
    ''')

    w(CPN / "Reporting" / "CPNReportManager.cs", r'''
        using System.Collections.Concurrent;
        using System.Net;
        using System.Security.Cryptography;
        using System.Text;
        using System.Text.Json;
        using NUnit.Framework;
        using NUnit.Framework.Interfaces;

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
                    OutputLines = SplitLines(result.Output),
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

            private static IReadOnlyList<string> SplitLines(string? output)
            {
                if (string.IsNullOrWhiteSpace(output))
                {
                    return Array.Empty<string>();
                }

                return output.Replace("\r\n", "\n", StringComparison.Ordinal)
                    .Split('\n', StringSplitOptions.RemoveEmptyEntries)
                    .ToList();
            }

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
    ''')

    w(CPN / "CPNReportManager.cs", '''
        namespace CVIS.Playwright.NUnitCompat;

        public static class CPNReportManager
        {
            public static string ReportRoot => Reporting.CPNReportManager.ReportRoot;
            public static string JsonReportPath => Reporting.CPNReportManager.JsonReportPath;
            public static string HtmlReportPath => Reporting.CPNReportManager.HtmlReportPath;
            public static string TestEntriesPath => Reporting.CPNReportManager.TestEntriesPath;

            public static void Initialize() => Reporting.CPNReportManager.Initialize();

            public static void RecordCurrentTest(NUnit.Framework.TestContext context, DateTimeOffset startedUtc) =>
                Reporting.CPNReportManager.RecordCurrentTest(context, startedUtc);

            public static void ResetForTesting(string? reportRoot = null) =>
                Reporting.CPNReportManager.ResetForTesting(reportRoot);
        }
    ''')

    w(CPNT / "Reporting" / "CPNReportManagerTests.cs", '''
        using System.Text.Json;
        using CVIS.Playwright.NUnitCompat.Reporting;

        namespace CVIS.Playwright.NUnitCompat.Tests.Reporting;

        [TestFixture]
        [Category("CPNReporting")]
        public sealed class CPNReportManagerTests
        {
            [Test]
            public void Record_ShouldWriteJsonHtmlAndPerTestEntry()
            {
                var reportRoot = Path.Combine(
                    TestContext.CurrentContext.WorkDirectory,
                    "TestResults",
                    "CPN-Unit-" + Guid.NewGuid().ToString("N"));

                CVIS.Playwright.NUnitCompat.Reporting.CPNReportManager.ResetForTesting(reportRoot);

                var entry = new CPNReportEntry
                {
                    Id = "sample-test",
                    TestName = "ShouldReport",
                    FullName = "CVIS.Tests.ShouldReport",
                    FixtureName = "CVIS.Tests",
                    Status = CPNReportStatus.Passed,
                    StartedUtc = DateTimeOffset.UtcNow.AddMilliseconds(-50),
                    FinishedUtc = DateTimeOffset.UtcNow,
                    DurationMilliseconds = 50,
                    Categories = new[] { "CPNReporting" }
                };

                CVIS.Playwright.NUnitCompat.Reporting.CPNReportManager.Record(entry);

                File.Exists(CVIS.Playwright.NUnitCompat.Reporting.CPNReportManager.JsonReportPath).Should().BeTrue();
                File.Exists(CVIS.Playwright.NUnitCompat.Reporting.CPNReportManager.HtmlReportPath).Should().BeTrue();

                var perTestFile = Path.Combine(
                    CVIS.Playwright.NUnitCompat.Reporting.CPNReportManager.TestEntriesPath,
                    "CVIS.Tests.ShouldReport.json");

                File.Exists(perTestFile).Should().BeTrue();

                var html = File.ReadAllText(CVIS.Playwright.NUnitCompat.Reporting.CPNReportManager.HtmlReportPath);
                html.Should().Contain("CPN Test Report");
                html.Should().Contain("CVIS.Tests.ShouldReport");

                var json = File.ReadAllText(CVIS.Playwright.NUnitCompat.Reporting.CPNReportManager.JsonReportPath);
                using var document = JsonDocument.Parse(json);

                document.RootElement.GetProperty("Total").GetInt32().Should().Be(1);
                document.RootElement.GetProperty("Passed").GetInt32().Should().Be(1);
                document.RootElement.GetProperty("Framework").GetString().Should().Be("CVIS.Playwright.NUnitCompat");
            }
        }
    ''')

    w(CPNT / "Reporting" / "CPNLifecycleReportOutputTests.cs", '''
        namespace CVIS.Playwright.NUnitCompat.Tests.Reporting;

        [TestFixture]
        [Category("CPNReporting")]
        public sealed class CPNLifecycleReportOutputTests : CVISPlaywrightTest
        {
            [Test]
            [Order(1)]
            public void CPNBaseClass_ShouldRunATestThatWillBeRecordedDuringTearDown()
            {
                Playwright.Should().NotBeNull();
                BrowserType.Should().NotBeNull();
                TestContext.WriteLine("CPN lifecycle report sample output.");
            }

            [Test]
            [Order(2)]
            public void CPNReportFiles_ShouldExistAfterCPNBaseClassTearDownHasRun()
            {
                File.Exists(CPNReportManager.JsonReportPath).Should().BeTrue();
                File.Exists(CPNReportManager.HtmlReportPath).Should().BeTrue();

                var html = File.ReadAllText(CPNReportManager.HtmlReportPath);
                html.Should().Contain("CPN Test Report");
                html.Should().Contain("CPNBaseClass_ShouldRunATestThatWillBeRecordedDuringTearDown");
            }
        }
    ''')

    print("Added CPN report output layer.")

if __name__ == "__main__":
    main()
