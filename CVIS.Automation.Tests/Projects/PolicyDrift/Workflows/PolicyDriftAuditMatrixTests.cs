using CVIS.Automation.Tests.Projects.PolicyDrift.Assertions;
using CVIS.Automation.Tests.Projects.PolicyDrift.Matrix;
using CVIS.Automation.Tests.Projects.PolicyDrift.Models;
using NUnit.Framework;
using CVIS.Automation.Tests.Shared.Playwright;
using CVIS.Automation.Tests.Shared.Reporting;

namespace CVIS.Automation.Tests.Projects.PolicyDrift.Workflows;

[TestFixture]
[Category("PolicyDrift")]
[Category("AuditRegression")]
[Category("WorkflowRegression")]
public sealed class PolicyDriftAuditMatrixTests : PlaywrightFunctionalTestBase
{
    [TestCaseSource(typeof(PolicyDriftScenarioData), nameof(PolicyDriftScenarioData.AuditCases))]
    public async Task AuditOrLogScenario_ShouldProduceExpectedRecord(PolicyDriftScenarioCase scenario)
    {
        await ConfirmPlaywrightRuntimeAsync();

        await ConfirmPlaywrightRuntimeAsync();

        await WriteRegressionReportAsync(
            project: "PolicyDrift",
            family: "audit/log",
            scenarioName: scenario.Name,
            scenarioType: scenario.ScenarioType,
            expectedBehavior: scenario.ExpectedBehavior,
            expectedFinalStatus: scenario.ExpectedFinalStatus,
            status: RegressionReportStatus.ScaffoldReady,
            details: "Playwright runtime confirmed. Scenario scaffold is ready for environment-specific wiring.");

        PolicyDriftScenarioAssert.MarkAsHarnessScaffold(scenario, "audit/log");
    }
}
