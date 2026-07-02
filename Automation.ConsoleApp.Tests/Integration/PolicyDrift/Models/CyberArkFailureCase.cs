namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Models;

public sealed record CyberArkFailureCase(
    string Name,
    int SimulatedStatusCode,
    string ExpectedBehavior)
{
    public override string ToString() => Name;
}
