using CVIS.Automation.Tests.Projects.PolicyDrift.Assertions;
using CVIS.Automation.Tests.Projects.PolicyDrift.Matrix;
using CVIS.Automation.Tests.Projects.PolicyDrift.Models;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Projects.PolicyDrift.Workflows;

[TestFixture]
[Category("PolicyDrift")]
[Category("CyberArk")]
[Category("ApiRegression")]
[Category("WorkflowRegression")]
public sealed class PolicyDriftCyberArkPolicyMatrixTests
{
    [TestCaseSource(typeof(PolicyDriftScenarioData), nameof(PolicyDriftScenarioData.CyberArkPolicyCases))]
    public void GetPolicyVariation_ShouldFollowExpectedBehavior(PolicyDriftScenarioCase scenario)
    {
        PolicyDriftScenarioAssert.MarkAsHarnessScaffold(scenario, "CyberArk GetPolicy");
    }
}
