using System.Collections.Concurrent;

namespace CVIS.FunctionalTesting.Reporting;

/// <summary>
/// Debug lifecycle log written from NUnit setup/teardown.
/// This is not the authoritative HyperExecute report source.
/// The authoritative report is built after dotnet test from TRX/NUnit XML.
/// </summary>
public static class TestLifecycleLog
{
    private static readonly ConcurrentBag<TestLifecycleEntry> Entries = new();

    public static void Record(TestLifecycleEntry entry)
    {
        Entries.Add(entry);
    }

    public static IReadOnlyList<TestLifecycleEntry> GetAll()
    {
        return Entries.ToArray();
    }

    public static void Clear()
    {
        while (Entries.TryTake(out _))
        {
        }
    }
}

public sealed record TestLifecycleEntry
{
    public required string TestName { get; init; }
    public required string FixtureClass { get; init; }
    public required string Outcome { get; init; }
    public string? Message { get; init; }
    public string? StackTrace { get; init; }
    public required double DurationMilliseconds { get; init; }
    public required DateTimeOffset StartedUtc { get; init; }
}
