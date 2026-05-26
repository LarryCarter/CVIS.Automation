using CVIS.Automation.Tests.Projects.PolicyDrift.Assertions;
using CVIS.Automation.Tests.Projects.PolicyDrift.Matrix;
using CVIS.Automation.Tests.Projects.PolicyDrift.Models;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Projects.PolicyDrift.Workflows;

[TestFixture]
[Category("PolicyDrift")]
[Category("CyberArk")]
[Category("Negative")]
[Category("WorkflowRegression")]
public sealed class PolicyDriftCyberArkPlatformMatrixTests
{
    [TestCaseSource(typeof(PolicyDriftScenarioData), nameof(PolicyDriftScenarioData.CyberArkPlatformCases))]
    public void GetPlatformsFailureOrVariation_ShouldFollowExpectedFallbackBehavior(PolicyDriftScenarioCase scenario)
    {
        PolicyDriftScenarioAssert.MarkAsHarnessScaffold(scenario, "CyberArk GetPlatforms");
    }
}
