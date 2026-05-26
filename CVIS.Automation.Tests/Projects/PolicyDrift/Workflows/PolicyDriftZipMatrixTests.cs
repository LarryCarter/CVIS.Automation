using CVIS.Automation.Tests.Projects.PolicyDrift.Assertions;
using CVIS.Automation.Tests.Projects.PolicyDrift.Matrix;
using CVIS.Automation.Tests.Projects.PolicyDrift.Models;
using NUnit.Framework;
using CVIS.Automation.Tests.Shared.Playwright;

namespace CVIS.Automation.Tests.Projects.PolicyDrift.Workflows;

[TestFixture]
[Category("PolicyDrift")]
[Category("ZipRegression")]
[Category("WorkflowRegression")]
public sealed class PolicyDriftZipMatrixTests : PlaywrightFunctionalTestBase
{
    [TestCaseSource(typeof(PolicyDriftScenarioData), nameof(PolicyDriftScenarioData.ZipCases))]
    public async Task ZipDownloadOrExtractionScenario_ShouldProduceExpectedBehavior(PolicyDriftScenarioCase scenario)
    {
        await ConfirmPlaywrightRuntimeAsync();

        PolicyDriftScenarioAssert.MarkAsHarnessScaffold(scenario, "ZIP handling");
    }
}
