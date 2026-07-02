using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Assertions;
using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Matrix;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Workflows;

public sealed class PolicyDriftCyberArkPolicyMatrixTests : UnitTestBase
{
    [Trait("Category", "PolicyDrift")]
    [Trait("Category", "CyberArk")]
    [Trait("Category", "ApiRegression")]
    [Trait("Category", "WorkflowRegression")]
    [Theory]
    [MemberData(nameof(PolicyDriftScenarioData.CyberArkPolicyCases), MemberType = typeof(PolicyDriftScenarioData))]
    public async Task GetPolicyVariation_ShouldFollowExpectedBehavior(
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

        PolicyDriftScenarioAssert.MarkAsHarnessScaffold(scenario, "CyberArk GetPolicy");
    }
}
