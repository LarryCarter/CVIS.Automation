using CVIS.Automation.Tests.Projects.PolicyDrift.Assertions;
using CVIS.Automation.Tests.Projects.PolicyDrift.Matrix;
using CVIS.Automation.Tests.Projects.PolicyDrift.Models;
using NUnit.Framework;
using CVIS.Automation.Tests.Shared.Playwright;

namespace CVIS.Automation.Tests.Projects.PolicyDrift.Workflows;

[TestFixture]
[Category("PolicyDrift")]
[Category("CyberArk")]
[Category("Negative")]
[Category("WorkflowRegression")]
public sealed class PolicyDriftCyberArkPlatformMatrixTests : PlaywrightFunctionalTestBase
{
    [TestCaseSource(typeof(PolicyDriftScenarioData), nameof(PolicyDriftScenarioData.CyberArkPlatformCases))]
    public async Task GetPlatformsFailureOrVariation_ShouldFollowExpectedFallbackBehavior(PolicyDriftScenarioCase scenario)
    {
        await ConfirmPlaywrightRuntimeAsync();

        PolicyDriftScenarioAssert.MarkAsHarnessScaffold(scenario, "CyberArk GetPlatforms");
    }
}
