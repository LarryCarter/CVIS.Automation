namespace CVIS.Playwright.Reporting.Models;

public sealed record CvisTestReportEntry
{
    public required string Id { get; init; }
    public required string TestName { get; init; }
    public required string FullName { get; init; }
    public required string FixtureName { get; init; }
    public required CvisTestReportStatus Status { get; init; }
    public required double DurationMilliseconds { get; init; }
    public string? Message { get; init; }
    public string? StackTrace { get; init; }
    public IReadOnlyList<string> Categories { get; init; } = Array.Empty<string>();
    public required string Source { get; init; }
    public required string SourceFile { get; init; }
}
