r"""
CVIS.Automation - Playwright Harness + Regression Report Patch

SAVE THIS FILE AS:
    C:\Users\larry\source\repos\CVIS.Automation\update_policy_drift_playwright_harness_and_report.py

RUN FROM:
    C:\Users\larry\source\repos\CVIS.Automation

COMMAND:
    python .\update_policy_drift_playwright_harness_and_report.py

THEN RUN:
    dotnet build .\CVIS.Automation.Tests\CVIS.Automation.Tests.csproj
    dotnet test .\CVIS.Automation.Tests\CVIS.Automation.Tests.csproj --filter TestCategory=PolicyDrift

REPORT OUTPUT:
    CVIS.Automation.Tests\bin\Debug\net8.0\TestReports\CVIS-Automation-Regression-Report.jsonl
    CVIS.Automation.Tests\bin\Debug\net8.0\TestReports\CVIS-Automation-Regression-Report.csv
"""

from __future__ import annotations

from pathlib import Path


SOLUTION_ROOT = Path.cwd()
TEST_PROJECT_ROOT = SOLUTION_ROOT / "CVIS.Automation.Tests"
POLICY_DRIFT_WORKFLOWS = TEST_PROJECT_ROOT / "Projects" / "PolicyDrift" / "Workflows"
SHARED_PLAYWRIGHT = TEST_PROJECT_ROOT / "Shared" / "Playwright"
SHARED_REPORTING = TEST_PROJECT_ROOT / "Shared" / "Reporting"


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def require_layout() -> None:
    if not TEST_PROJECT_ROOT.exists():
        raise RuntimeError(
            "Cannot find CVIS.Automation.Tests. Run this from:\n"
            r"    C:\Users\larry\source\repos\CVIS.Automation"
        )

    if not POLICY_DRIFT_WORKFLOWS.exists():
        raise RuntimeError(
            "Cannot find PolicyDrift workflow test folder:\n"
            f"    {POLICY_DRIFT_WORKFLOWS}\n"
            "Run the PolicyDrift regression pack generator first."
        )


def write_playwright_harness() -> None:
    write_text(
        SHARED_PLAYWRIGHT / "PlaywrightFunctionalTestBase.cs",
        """using CVIS.Automation.Tests.Shared.Reporting;
using Microsoft.Playwright;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Shared.Playwright;

public abstract class PlaywrightFunctionalTestBase
{
    protected IPlaywright PlaywrightRuntime { get; private set; } = null!;
    protected IAPIRequestContext PlaywrightRequestContext { get; private set; } = null!;

    [SetUp]
    public async Task PlaywrightFunctionalSetupAsync()
    {
        PlaywrightRuntime = await Microsoft.Playwright.Playwright.CreateAsync();

        PlaywrightRequestContext = await PlaywrightRuntime.APIRequest.NewContextAsync(
            new APIRequestNewContextOptions
            {
                IgnoreHTTPSErrors = true
            });
    }

    [TearDown]
    public async Task PlaywrightFunctionalTearDownAsync()
    {
        if (PlaywrightRequestContext is not null)
        {
            await PlaywrightRequestContext.DisposeAsync();
        }

        PlaywrightRuntime?.Dispose();
    }

    protected async Task ConfirmPlaywrightRuntimeAsync()
    {
        Assert.That(
            PlaywrightRuntime,
            Is.Not.Null,
            "Playwright runtime must be initialized for this functional regression test.");

        Assert.That(
            PlaywrightRequestContext,
            Is.Not.Null,
            "Playwright APIRequestContext must be initialized for this functional regression test.");

        await Task.CompletedTask;
    }

    protected async Task WriteRegressionReportAsync(
        string project,
        string family,
        string scenarioName,
        string scenarioType,
        string expectedBehavior,
        string expectedFinalStatus,
        RegressionReportStatus status,
        string details)
    {
        await RegressionReportWriter.WriteAsync(
            new RegressionReportEntry
            {
                Project = project,
                Family = family,
                ScenarioName = scenarioName,
                ScenarioType = scenarioType,
                ExpectedBehavior = expectedBehavior,
                ExpectedFinalStatus = expectedFinalStatus,
                Status = status.ToString(),
                Details = details,
                UsesPlaywright = PlaywrightRuntime is not null && PlaywrightRequestContext is not null,
                TimestampUtc = DateTime.UtcNow
            });
    }
}
""",
    )


def write_reporting_files() -> None:
    write_text(
        SHARED_REPORTING / "RegressionReportStatus.cs",
        """namespace CVIS.Automation.Tests.Shared.Reporting;

public enum RegressionReportStatus
{
    ScaffoldReady,
    Passed,
    Failed,
    Skipped,
    NeedsWiring
}
""",
    )

    write_text(
        SHARED_REPORTING / "RegressionReportEntry.cs",
        """namespace CVIS.Automation.Tests.Shared.Reporting;

public sealed class RegressionReportEntry
{
    public DateTime TimestampUtc { get; init; }
    public string Project { get; init; } = string.Empty;
    public string Family { get; init; } = string.Empty;
    public string ScenarioName { get; init; } = string.Empty;
    public string ScenarioType { get; init; } = string.Empty;
    public string ExpectedBehavior { get; init; } = string.Empty;
    public string ExpectedFinalStatus { get; init; } = string.Empty;
    public string Status { get; init; } = string.Empty;
    public bool UsesPlaywright { get; init; }
    public string Details { get; init; } = string.Empty;
}
""",
    )

    write_text(
        SHARED_REPORTING / "RegressionReportWriter.cs",
        """using System.Text;
using System.Text.Json;

namespace CVIS.Automation.Tests.Shared.Reporting;

public static class RegressionReportWriter
{
    private static readonly SemaphoreSlim Gate = new(1, 1);

    public static string ReportDirectory =>
        Path.Combine(AppContext.BaseDirectory, "TestReports");

    public static string JsonLinesReportPath =>
        Path.Combine(ReportDirectory, "CVIS-Automation-Regression-Report.jsonl");

    public static string CsvReportPath =>
        Path.Combine(ReportDirectory, "CVIS-Automation-Regression-Report.csv");

    public static async Task WriteAsync(RegressionReportEntry entry)
    {
        Directory.CreateDirectory(ReportDirectory);

        await Gate.WaitAsync();

        try
        {
            await WriteJsonLineAsync(entry);
            await WriteCsvLineAsync(entry);
        }
        finally
        {
            Gate.Release();
        }
    }

    private static async Task WriteJsonLineAsync(RegressionReportEntry entry)
    {
        var json = JsonSerializer.Serialize(
            entry,
            new JsonSerializerOptions
            {
                WriteIndented = false
            });

        await File.AppendAllTextAsync(
            JsonLinesReportPath,
            json + Environment.NewLine,
            Encoding.UTF8);
    }

    private static async Task WriteCsvLineAsync(RegressionReportEntry entry)
    {
        var fileExists = File.Exists(CsvReportPath);

        await using var stream = new FileStream(
            CsvReportPath,
            FileMode.Append,
            FileAccess.Write,
            FileShare.ReadWrite);

        await using var writer = new StreamWriter(stream, Encoding.UTF8);

        if (!fileExists)
        {
            await writer.WriteLineAsync(
                "TimestampUtc,Project,Family,ScenarioName,ScenarioType,ExpectedBehavior,ExpectedFinalStatus,Status,UsesPlaywright,Details");
        }

        await writer.WriteLineAsync(string.Join(
            ",",
            Escape(entry.TimestampUtc.ToString("O")),
            Escape(entry.Project),
            Escape(entry.Family),
            Escape(entry.ScenarioName),
            Escape(entry.ScenarioType),
            Escape(entry.ExpectedBehavior),
            Escape(entry.ExpectedFinalStatus),
            Escape(entry.Status),
            Escape(entry.UsesPlaywright.ToString()),
            Escape(entry.Details)));
    }

    private static string Escape(string value)
    {
        var safe = value
            .Replace("\"", "\"\"")
            .Replace("\\r", " ")
            .Replace("\\n", " ");

        return $"\"{safe}\"";
    }
}
""",
    )


def patch_matrix_file(path: Path, family: str) -> None:
    text = path.read_text(encoding="utf-8")

    if "using CVIS.Automation.Tests.Shared.Playwright;" not in text:
        text = text.replace(
            "using NUnit.Framework;",
            "using NUnit.Framework;\nusing CVIS.Automation.Tests.Shared.Playwright;\nusing CVIS.Automation.Tests.Shared.Reporting;",
        )

    if "using CVIS.Automation.Tests.Shared.Reporting;" not in text:
        text = text.replace(
            "using CVIS.Automation.Tests.Shared.Playwright;",
            "using CVIS.Automation.Tests.Shared.Playwright;\nusing CVIS.Automation.Tests.Shared.Reporting;",
        )

    if ": PlaywrightFunctionalTestBase" not in text:
        lines = text.splitlines()
        for index, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("public sealed class ") and ":" not in stripped:
                lines[index] = line + " : PlaywrightFunctionalTestBase"
                break
        text = "\n".join(lines) + "\n"

    text = text.replace("    public void ", "    public async Task ")

    marker_prefix = "        PolicyDriftScenarioAssert.MarkAsHarnessScaffold(scenario,"
    if marker_prefix in text and "WriteRegressionReportAsync(" not in text:
        text = text.replace(
            marker_prefix,
            f"""        await ConfirmPlaywrightRuntimeAsync();

        await WriteRegressionReportAsync(
            project: "PolicyDrift",
            family: "{family}",
            scenarioName: scenario.Name,
            scenarioType: scenario.ScenarioType,
            expectedBehavior: scenario.ExpectedBehavior,
            expectedFinalStatus: scenario.ExpectedFinalStatus,
            status: RegressionReportStatus.ScaffoldReady,
            details: "Playwright runtime confirmed. Scenario scaffold is ready for environment-specific wiring.");

        PolicyDriftScenarioAssert.MarkAsHarnessScaffold(scenario,""",
        )

    path.write_text(text, encoding="utf-8")


def patch_policy_drift_matrix_tests() -> None:
    files = {
        "PolicyDriftCyberArkPlatformMatrixTests.cs": "CyberArk GetPlatforms",
        "PolicyDriftCyberArkPolicyMatrixTests.cs": "CyberArk GetPolicy",
        "PolicyDriftDbFallbackMatrixTests.cs": "DB fallback",
        "PolicyDriftZipMatrixTests.cs": "ZIP handling",
        "PolicyDriftJobMatrixTests.cs": "scheduled job",
        "PolicyDriftProcessingMatrixTests.cs": "policy processing",
        "PolicyDriftAuditMatrixTests.cs": "audit/log",
        "PolicyDriftReportMatrixTests.cs": "report output",
    }

    for file_name, family in files.items():
        path = POLICY_DRIFT_WORKFLOWS / file_name
        if path.exists():
            patch_matrix_file(path, family)
        else:
            print(f"WARNING: Missing expected matrix file: {path}")


def main() -> None:
    require_layout()
    write_playwright_harness()
    write_reporting_files()
    patch_policy_drift_matrix_tests()

    print()
    print("Updated PolicyDrift tests with Playwright harness and regression report output.")
    print()
    print("Created/updated:")
    print(f"  {SHARED_PLAYWRIGHT / 'PlaywrightFunctionalTestBase.cs'}")
    print(f"  {SHARED_REPORTING / 'RegressionReportStatus.cs'}")
    print(f"  {SHARED_REPORTING / 'RegressionReportEntry.cs'}")
    print(f"  {SHARED_REPORTING / 'RegressionReportWriter.cs'}")
    print()
    print("Patched PolicyDrift matrix tests under:")
    print(f"  {POLICY_DRIFT_WORKFLOWS}")
    print()
    print("Next commands:")
    print(r"  dotnet build .\CVIS.Automation.Tests\CVIS.Automation.Tests.csproj")
    print(r"  dotnet test .\CVIS.Automation.Tests\CVIS.Automation.Tests.csproj --filter TestCategory=PolicyDrift")
    print()
    print("Report output after test run:")
    print(r"  .\CVIS.Automation.Tests\bin\Debug\net8.0\TestReports\CVIS-Automation-Regression-Report.jsonl")
    print(r"  .\CVIS.Automation.Tests\bin\Debug\net8.0\TestReports\CVIS-Automation-Regression-Report.csv")
    print()


if __name__ == "__main__":
    main()
