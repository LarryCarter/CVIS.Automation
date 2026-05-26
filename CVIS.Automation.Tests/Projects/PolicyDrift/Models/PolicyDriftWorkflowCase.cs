namespace CVIS.Automation.Tests.Projects.PolicyDrift.Models;

public sealed record PolicyDriftWorkflowCase(
    string Name,
    string ScenarioType,
    string ExpectedFinalStatus,
    int ExpectedMinimumDriftCount);
