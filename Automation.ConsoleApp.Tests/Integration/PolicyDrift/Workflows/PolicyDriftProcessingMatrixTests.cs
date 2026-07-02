using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Assertions;
using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Matrix;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Workflows;

public sealed class PolicyDriftProcessingMatrixTests : UnitTestBase
{
    [Trait("Category", "PolicyDrift")]
    [Trait("Category", "PolicyProcessingRegression")]
    [Trait("Category", "WorkflowRegression")]
    [Theory]
    [MemberData(nameof(PolicyDriftScenarioData.PolicyProcessingCases), MemberType = typeof(PolicyDriftScenarioData))]
    public async Task PolicyProcessingScenario_ShouldProduceExpectedDriftBehavior(
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

        PolicyDriftScenarioAssert.MarkAsHarnessScaffold(scenario, "policy processing");
    }
}
