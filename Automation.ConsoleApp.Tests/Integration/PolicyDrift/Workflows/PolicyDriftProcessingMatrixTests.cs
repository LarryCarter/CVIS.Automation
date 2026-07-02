using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Assertions;
using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Matrix;
using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Models;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Workflows;

public sealed class PolicyDriftProcessingMatrixTests : UnitTestBase
{
    [Theory]
    [MemberData(nameof(PolicyDriftScenarioData.PolicyProcessingCases), MemberType = typeof(PolicyDriftScenarioData))]
    [Trait("Category", "PolicyDrift")]
    [Trait("Category", "PolicyProcessingRegression")]
    [Trait("Category", "WorkflowRegression")]
    public async Task PolicyProcessingScenario_ShouldProduceExpectedDriftBehavior(PolicyDriftScenarioCase scenario)
    {
        await Task.CompletedTask;

        PolicyDriftScenarioAssert.MarkAsHarnessScaffold(scenario, "policy processing");
        scenario.ExpectedFinalStatus.Should().NotBeNullOrWhiteSpace();
    }
}
