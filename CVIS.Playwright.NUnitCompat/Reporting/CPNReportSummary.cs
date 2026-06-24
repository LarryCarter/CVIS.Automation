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
