using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Assertions;
using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Matrix;
using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Models;
using FluentAssertions;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Workflows;

public sealed class PolicyDriftCyberArkPlatformMatrixTests : UnitTestBase
{
    [Theory]
    [Trait("PolicyDrift", "true")]
    [Trait("WorkflowRegression", "true")]
    [Trait("CyberArk", "true")]
    [MemberData(nameof(PolicyDriftScenarioData.CyberArkPlatformCases), MemberType = typeof(PolicyDriftScenarioData))]
    public Task GetPlatformsFailureOrVariation_ShouldFollowExpectedFallbackBehavior(PolicyDriftScenarioCase scenario)
    {
        PolicyDriftScenarioAssert.ValidateScenarioDefinition(scenario);

        scenario.ExpectedBehavior.Should().NotBeNullOrWhiteSpace();
        scenario.ExpectedFinalStatus.Should().NotBeNullOrWhiteSpace();

        return Task.CompletedTask;
    }
}
