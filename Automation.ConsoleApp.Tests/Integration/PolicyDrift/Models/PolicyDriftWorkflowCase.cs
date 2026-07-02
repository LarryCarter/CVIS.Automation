namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Models;

public sealed record PolicyDriftWorkflowCase(
    string Name,
    string ScenarioType,
    string ExpectedFinalStatus,
    int ExpectedMinimumDriftCount);
