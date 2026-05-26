namespace CVIS.Automation.Tests.Projects.PolicyDrift.Models;

public sealed record CyberArkFailureCase(
    string Name,
    int SimulatedStatusCode,
    string ExpectedBehavior);
