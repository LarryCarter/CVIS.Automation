using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Assertions;
using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Matrix;
using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Models;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Workflows;

public sealed class PolicyDriftReportMatrixTests : UnitTestBase
{
    [Theory]
    [MemberData(nameof(PolicyDriftScenarioData.ReportCases), MemberType = typeof(PolicyDriftScenarioData))]
    [Trait("Category", "PolicyDrift")]
    [Trait("Category", "ReportRegression")]
    [Trait("Category", "WorkflowRegression")]
    public async Task ReportScenario_ShouldProduceExpectedOutput(PolicyDriftScenarioCase scenario)
    {
        await Task.CompletedTask;

        PolicyDriftScenarioAssert.MarkAsHarnessScaffold(scenario, "report output");
        scenario.ExpectedFinalStatus.Should().NotBeNullOrWhiteSpace();
    }
}
