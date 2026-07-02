namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Models;

public sealed record PolicyDriftScenarioCase
{
    public string Name { get; init; } = string.Empty;
    public string ScenarioType { get; init; } = string.Empty;
    public string ExpectedBehavior { get; init; } = string.Empty;
    public string ExpectedFinalStatus { get; init; } = string.Empty;
    public int ExpectedMinimumRecordCount { get; init; }
}
