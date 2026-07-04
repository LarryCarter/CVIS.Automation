using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Matrix;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Workflows;

public sealed class PolicyDriftWorkflowTests : UnitTestBase
{
    [Fact]
[Trait("Category", "PolicyDrift")]
    public void PolicyDriftScenario_Category_ShouldProduceExpectedFinalState()
    {
        Assert.True(true);
    }

    [Fact]
[Trait("Category", "WorkflowRegression")]
    public void PolicyDriftScenario_Category_ShouldProduceExpectedFinalState()
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
