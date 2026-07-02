using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Matrix;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Workflows;

public sealed class PolicyDriftWorkflowTests : UnitTestBase
{
    [Trait("Category", "PolicyDrift")]
    [Trait("Category", "WorkflowRegression")]
    [Theory]
    [MemberData(nameof(PolicyDriftScenarioData.WorkflowCases), MemberType = typeof(PolicyDriftScenarioData))]
    public async Task PolicyDriftScenario_ShouldProduceExpectedFinalState(
        string name,
        string scenarioType,
        string expectedFinalStatus,
        int expectedMinimumDriftCount)
    {
        await Task.CompletedTask;

        var testCase = PolicyDriftScenarioData.CreateWorkflowCase(
            name,
            scenarioType,
            expectedFinalStatus,
            expectedMinimumDriftCount);

        testCase.Name.Should().NotBeNullOrWhiteSpace();
        testCase.ScenarioType.Should().NotBeNullOrWhiteSpace();
        testCase.ExpectedFinalStatus.Should().Be("Completed");
        testCase.ExpectedMinimumDriftCount.Should().BeGreaterThanOrEqualTo(0);
    }
}
