using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Assertions;
using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Matrix;
using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Models;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Workflows;

public sealed class PolicyDriftZipMatrixTests : UnitTestBase
{
    [Theory]
    [Trait("PolicyDrift", "true")]
    [Trait("Category", "ZipRegression")]
    [Trait("Category", "WorkflowRegression")]
    [MemberData(nameof(PolicyDriftScenarioData.ZipCases), MemberType = typeof(PolicyDriftScenarioData))]
    public async Task ZipDownloadOrExtractionScenario_ShouldProduceExpectedBehavior(PolicyDriftScenarioCase scenario)
    {
        await ConfirmPlaywrightRuntimeAsync();

        await WriteRegressionReportAsync(
            project: "PolicyDrift",
            family: "ZIP handling",
            scenarioName: scenario.Name,
            scenarioType: scenario.ScenarioType,
            expectedBehavior: scenario.ExpectedBehavior,
            expectedFinalStatus: scenario.ExpectedFinalStatus,
            status: UnitTestData.ScaffoldReady,
            details: "xUnit scenario data loaded. Scenario scaffold is ready for environment-specific wiring.");

        PolicyDriftScenarioAssert.MarkAsHarnessScaffold(scenario, "ZIP handling");
    }
}
