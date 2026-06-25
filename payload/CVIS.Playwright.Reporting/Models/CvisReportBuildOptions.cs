namespace CVIS.Playwright.Reporting.Models;

public sealed record CvisReportBuildOptions
{
    public required string FrameworkName { get; init; }
    public required string TrxRoot { get; init; }
    public required string NUnitXmlRoot { get; init; }
    public required string OutputRoot { get; init; }
    public int MinimumTotal { get; init; } = 1;
}
