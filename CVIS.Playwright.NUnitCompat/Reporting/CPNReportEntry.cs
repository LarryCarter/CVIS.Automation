namespace CVIS.Playwright.NUnitCompat.Reporting;

public sealed record CPNReportEntry
{
    public required string Id { get; init; }
    public required string TestName { get; init; }
    public required string FullName { get; init; }
    public required string FixtureName { get; init; }
    public required CPNReportStatus Status { get; init; }
    public required DateTimeOffset StartedUtc { get; init; }
    public required DateTimeOffset FinishedUtc { get; init; }
    public required double DurationMilliseconds { get; init; }
    public string? Message { get; init; }
    public string? StackTrace { get; init; }
    public string? WorkerId { get; init; }
    public string? BrowserName { get; init; }
    public IReadOnlyList<string> Categories { get; init; } = Array.Empty<string>();
    public IReadOnlyList<string> OutputLines { get; init; } = Array.Empty<string>();
    public IReadOnlyList<string> Attachments { get; init; } = Array.Empty<string>();
}
