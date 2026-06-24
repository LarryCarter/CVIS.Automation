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
