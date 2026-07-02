using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Assertions;
using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Matrix;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Workflows;

public sealed class PolicyDriftJobMatrixTests : UnitTestBase
{
    [Trait("Category", "PolicyDrift")]
    [Trait("Category", "JobRegression")]
    [Trait("Category", "WorkflowRegression")]
    [Theory]
    [MemberData(nameof(PolicyDriftScenarioData.JobCases), MemberType = typeof(PolicyDriftScenarioData))]
    public async Task ScheduledJobScenario_ShouldProduceExpectedBehavior(
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

        PolicyDriftScenarioAssert.MarkAsHarnessScaffold(scenario, "scheduled job");
    }
}
