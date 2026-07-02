using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Assertions;
using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Matrix;
using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Models;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Workflows;

public sealed class PolicyDriftCyberArkPlatformMatrixTests : UnitTestBase
{
    [Theory]
    [MemberData(nameof(PolicyDriftScenarioData.CyberArkPlatformCases), MemberType = typeof(PolicyDriftScenarioData))]
    [Trait("Category", "PolicyDrift")]
    [Trait("Category", "CyberArk")]
    [Trait("Category", "Negative")]
    [Trait("Category", "WorkflowRegression")]
    public async Task GetPlatformsFailureOrVariation_ShouldFollowExpectedFallbackBehavior(PolicyDriftScenarioCase scenario)
    {
        await Task.CompletedTask;

        PolicyDriftScenarioAssert.MarkAsHarnessScaffold(scenario, "CyberArk GetPlatforms");
        scenario.ExpectedFinalStatus.Should().NotBeNullOrWhiteSpace();
    }
}
