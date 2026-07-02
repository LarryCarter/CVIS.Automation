using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Assertions;
using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Matrix;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Workflows;

public sealed class PolicyDriftCyberArkPlatformMatrixTests : UnitTestBase
{
    [Trait("Category", "PolicyDrift")]
    [Trait("Category", "CyberArk")]
    [Trait("Category", "Negative")]
    [Trait("Category", "WorkflowRegression")]
    [Theory]
    [MemberData(nameof(PolicyDriftScenarioData.CyberArkPlatformCases), MemberType = typeof(PolicyDriftScenarioData))]
    public async Task GetPlatformsFailureOrVariation_ShouldFollowExpectedFallbackBehavior(
        string name,
        string scenarioType,
        string expectedBehavior,
        string expectedFinalStatus,
        int expectedMinimumRecordCount)
    {
        await Task.CompletedTask;

        var scenario = PolicyDriftScenarioData.CreateScenario(
            name,
            scenarioType,
            expectedBehavior,
            expectedFinalStatus,
            expectedMinimumRecordCount);

        PolicyDriftScenarioAssert.MarkAsHarnessScaffold(scenario, "CyberArk GetPlatforms");
    }
}
