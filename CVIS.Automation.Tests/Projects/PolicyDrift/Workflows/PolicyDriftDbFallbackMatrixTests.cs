using CVIS.Automation.Tests.Projects.PolicyDrift.Assertions;
using CVIS.Automation.Tests.Projects.PolicyDrift.Matrix;
using CVIS.Automation.Tests.Projects.PolicyDrift.Models;
using NUnit.Framework;
using CVIS.Automation.Tests.Shared.Playwright;

namespace CVIS.Automation.Tests.Projects.PolicyDrift.Workflows;

[TestFixture]
[Category("PolicyDrift")]
[Category("DatabaseRegression")]
[Category("WorkflowRegression")]
public sealed class PolicyDriftDbFallbackMatrixTests : PlaywrightFunctionalTestBase
{
    [TestCaseSource(typeof(PolicyDriftScenarioData), nameof(PolicyDriftScenarioData.DbFallbackCases))]
    public async Task DatabaseFallbackScenario_ShouldProduceExpectedBehavior(PolicyDriftScenarioCase scenario)
    {
        await ConfirmPlaywrightRuntimeAsync();

        PolicyDriftScenarioAssert.MarkAsHarnessScaffold(scenario, "DB fallback");
    }
}
