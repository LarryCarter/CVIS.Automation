using CVIS.Automation.Tests.Projects.PolicyDrift.Assertions;
using CVIS.Automation.Tests.Projects.PolicyDrift.Matrix;
using CVIS.Automation.Tests.Projects.PolicyDrift.Models;
using NUnit.Framework;
using CVIS.Automation.Tests.Shared.Playwright;
using CVIS.Automation.Tests.Shared.Reporting;

namespace CVIS.Automation.Tests.Projects.PolicyDrift.Workflows;

[TestFixture]
[Category("PolicyDrift")]
[Category("ReportRegression")]
[Category("WorkflowRegression")]
public sealed class PolicyDriftReportMatrixTests : PlaywrightFunctionalTestBase
{
    [TestCaseSource(typeof(PolicyDriftScenarioData), nameof(PolicyDriftScenarioData.ReportCases))]
    public async Task ReportScenario_ShouldProduceExpectedOutput(PolicyDriftScenarioCase scenario)
    {
        await ConfirmPlaywrightRuntimeAsync();

        await ConfirmPlaywrightRuntimeAsync();

        await WriteRegressionReportAsync(
            project: "PolicyDrift",
            family: "report output",
            scenarioName: scenario.Name,
            scenarioType: scenario.ScenarioType,
            expectedBehavior: scenario.ExpectedBehavior,
            expectedFinalStatus: scenario.ExpectedFinalStatus,
            status: RegressionReportStatus.ScaffoldReady,
            details: "Playwright runtime confirmed. Scenario scaffold is ready for environment-specific wiring.");

        PolicyDriftScenarioAssert.MarkAsHarnessScaffold(scenario, "report output");
    }
}
