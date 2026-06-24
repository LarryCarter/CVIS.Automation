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
