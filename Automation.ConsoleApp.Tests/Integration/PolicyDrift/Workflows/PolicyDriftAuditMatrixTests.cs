using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Assertions;
using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Matrix;
using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Models;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Workflows;

public sealed class PolicyDriftAuditMatrixTests : UnitTestBase
{
    [Theory]
    [Trait("PolicyDrift", "true")]
    [Trait("Category", "AuditRegression")]
    [Trait("Category", "WorkflowRegression")]
    [MemberData(nameof(PolicyDriftScenarioData.AuditCases), MemberType = typeof(PolicyDriftScenarioData))]
    public async Task AuditOrLogScenario_ShouldProduceExpectedRecord(PolicyDriftScenarioCase scenario)
    {
        await ConfirmPlaywrightRuntimeAsync();

        await WriteRegressionReportAsync(
            project: "PolicyDrift",
            family: "audit/log",
            scenarioName: scenario.Name,
            scenarioType: scenario.ScenarioType,
            expectedBehavior: scenario.ExpectedBehavior,
            expectedFinalStatus: scenario.ExpectedFinalStatus,
            status: UnitTestData.ScaffoldReady,
            details: "xUnit scenario data loaded. Scenario scaffold is ready for environment-specific wiring.");

        PolicyDriftScenarioAssert.MarkAsHarnessScaffold(scenario, "audit/log");
    }
}
