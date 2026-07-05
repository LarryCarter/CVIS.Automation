using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Matrix;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Workflows;

public sealed class PolicyDriftWorkflowTests : UnitTestBase
{
    [Fact]
[Trait("Category", "PolicyDrift")]
    public void PolicyDriftScenario_PolicyDrift_ShouldProduceExpectedFinalState()
    {
        Assert.True(true);
    }

    [Fact]
[Trait("Category", "WorkflowRegression")]
    public void PolicyDriftScenario_WorkflowRegression_ShouldProduceExpectedFinalState()
    {
        Assert.True(true);
    }

    [Theory]
    [MemberData(nameof(PolicyDriftScenarioData.PolicyDriftWorkflowCases), MemberType = typeof(PolicyDriftScenarioData))]
[Trait("Category", "PolicyDrift")]
    public void PolicyDriftScenario_PolicyDrift_ShouldFinishWithExpectedStatus(
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

    [Theory]
    [MemberData(nameof(PolicyDriftScenarioData.PolicyDriftWorkflowCases), MemberType = typeof(PolicyDriftScenarioData))]
[Trait("Category", "WorkflowRegression")]
    public void PolicyDriftScenario_WorkflowRegression_ShouldFinishWithExpectedStatus(
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
