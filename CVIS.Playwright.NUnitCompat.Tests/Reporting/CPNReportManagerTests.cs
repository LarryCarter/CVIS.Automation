using System.Text.Json;
using CVIS.Playwright.NUnitCompat.Reporting;
using CVIS.Playwright.NUnitCompat;

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
