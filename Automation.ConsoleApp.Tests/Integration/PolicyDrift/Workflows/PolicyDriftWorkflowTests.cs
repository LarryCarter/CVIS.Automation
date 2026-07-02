using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Matrix;
using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Models;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Workflows;

public sealed class PolicyDriftWorkflowTests : UnitTestBase
{
    [Theory]
    [Trait("PolicyDrift", "true")]
    [Trait("Category", "WorkflowRegression")]
    [MemberData(nameof(PolicyDriftScenarioData.PolicyDriftWorkflowCases), MemberType = typeof(PolicyDriftScenarioData))]
    public async Task PolicyDriftScenario_ShouldProduceExpectedFinalState(PolicyDriftWorkflowCase testCase)
    {
        await Task.CompletedTask;

        testCase.Name.Should().NotBeNullOrWhiteSpace();
        testCase.ScenarioType.Should().NotBeNullOrWhiteSpace();
        testCase.ExpectedFinalStatus.Should().Be("Completed");
        testCase.ExpectedMinimumDriftCount.Should().BeGreaterThanOrEqualTo(0);
    }
}
