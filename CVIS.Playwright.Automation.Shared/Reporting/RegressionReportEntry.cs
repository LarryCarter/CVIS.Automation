namespace CVIS.Playwright.Automation.Shared.Reporting;

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
