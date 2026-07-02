using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Models;
using FluentAssertions;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Assertions;

public static class PolicyDriftScenarioAssert
{
    public static void ValidateScenarioDefinition(PolicyDriftScenarioCase scenario)
    {
        scenario.Name.Should().NotBeNullOrWhiteSpace();
        scenario.ScenarioType.Should().NotBeNullOrWhiteSpace();
        scenario.ExpectedBehavior.Should().NotBeNullOrWhiteSpace();
        scenario.ExpectedMinimumRecordCount.Should().BeGreaterThanOrEqualTo(0);
    }

    public static void ValidateWorkflowDefinition(PolicyDriftWorkflowCase scenario)
    {
        scenario.Name.Should().NotBeNullOrWhiteSpace();
        scenario.ScenarioType.Should().NotBeNullOrWhiteSpace();
        scenario.ExpectedFinalStatus.Should().NotBeNullOrWhiteSpace();
        scenario.ExpectedMinimumDriftCount.Should().BeGreaterThanOrEqualTo(0);
    }

    public static void ValidateCyberArkFailureDefinition(CyberArkFailureCase scenario)
    {
        scenario.Name.Should().NotBeNullOrWhiteSpace();
        scenario.ExpectedBehavior.Should().NotBeNullOrWhiteSpace();
        scenario.SimulatedStatusCode.Should().BeGreaterThanOrEqualTo(0);
    }
}
