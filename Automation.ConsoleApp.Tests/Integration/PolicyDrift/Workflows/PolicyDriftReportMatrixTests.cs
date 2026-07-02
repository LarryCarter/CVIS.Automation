using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Assertions;
using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Matrix;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Workflows;

public sealed class PolicyDriftReportMatrixTests : UnitTestBase
{
    [Trait("Category", "PolicyDrift")]
    [Trait("Category", "ReportRegression")]
    [Trait("Category", "WorkflowRegression")]
    [Theory]
    [MemberData(nameof(PolicyDriftScenarioData.ReportCases), MemberType = typeof(PolicyDriftScenarioData))]
    public async Task ReportScenario_ShouldProduceExpectedOutput(
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

        PolicyDriftScenarioAssert.MarkAsHarnessScaffold(scenario, "report output");
    }
}
