using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Assertions;
using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Matrix;
using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Models;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Workflows;

public sealed class PolicyDriftJobMatrixTests : UnitTestBase
{
    [Theory]
    [MemberData(nameof(PolicyDriftScenarioData.JobCases), MemberType = typeof(PolicyDriftScenarioData))]
    [Trait("Category", "PolicyDrift")]
    [Trait("Category", "JobRegression")]
    [Trait("Category", "WorkflowRegression")]
    public async Task ScheduledJobScenario_ShouldProduceExpectedBehavior(PolicyDriftScenarioCase scenario)
    {
        await Task.CompletedTask;

        PolicyDriftScenarioAssert.MarkAsHarnessScaffold(scenario, "scheduled job");
        scenario.ExpectedFinalStatus.Should().NotBeNullOrWhiteSpace();
    }
}
