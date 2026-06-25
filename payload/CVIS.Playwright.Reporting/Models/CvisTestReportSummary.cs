namespace CVIS.Playwright.Reporting.Models;

public sealed record CvisTestReportSummary
{
    public required string Framework { get; init; }
    public required string Source { get; init; }
    public required DateTimeOffset GeneratedUtc { get; init; }
    public required int Total { get; init; }
    public required int Passed { get; init; }
    public required int Failed { get; init; }
    public required int Skipped { get; init; }
    public required int Other { get; init; }
    public required IReadOnlyList<CvisTestReportEntry> Tests { get; init; }
}
