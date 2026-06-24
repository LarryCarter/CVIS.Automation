using CVIS.Playwright.NUnitCompat;
namespace CVIS.Playwright.NUnitCompat.Reporting;

public sealed record CPNReportOptions
{
    public bool Enabled { get; init; } = true;
    public string ReportRoot { get; init; } = string.Empty;
    public string JsonFileName { get; init; } = "cpn-lifecycle-report.json";
    public string HtmlFileName { get; init; } = "cpn-lifecycle-report.html";

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
