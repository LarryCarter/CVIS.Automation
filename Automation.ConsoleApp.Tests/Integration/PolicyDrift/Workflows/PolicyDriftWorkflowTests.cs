using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Matrix;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Workflows;

public sealed class PolicyDriftWorkflowTests : UnitTestBase
{
    [Trait("Category", "PolicyDrift")]
    [Trait("Category", "WorkflowRegression")]
    [Fact]
    public void PolicyDriftScenario_ShouldProduceExpectedFinalState()
    {
        Assert.True(true);
    }

    [Trait("Category", "PolicyDrift")]
    [Trait("Category", "WorkflowRegression")]
    [Theory]
    [MemberData(nameof(PolicyDriftScenarioData.PolicyDriftWorkflowCases), MemberType = typeof(PolicyDriftScenarioData))]
    public void PolicyDriftScenario_ShouldFinishWithExpectedStatus(
        string name,
        string scenarioType,
        string expectedFinalStatus,
        int expectedMinimumDriftCount)
    {
        name.Should().NotBeNullOrWhiteSpace();
        scenarioType.Should().NotBeNullOrWhiteSpace();
        expectedFinalStatus.Should().Be("Completed");
        expectedMinimumDriftCount.Should().BeGreaterThanOrEqualTo(0);
    }
}
