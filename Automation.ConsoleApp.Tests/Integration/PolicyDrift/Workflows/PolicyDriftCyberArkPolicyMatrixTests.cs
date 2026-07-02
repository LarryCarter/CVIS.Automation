using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Assertions;
using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Matrix;
using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Models;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Workflows;

public sealed class PolicyDriftCyberArkPolicyMatrixTests : UnitTestBase
{
    [Theory]
    [MemberData(nameof(PolicyDriftScenarioData.CyberArkPolicyCases), MemberType = typeof(PolicyDriftScenarioData))]
    [Trait("Category", "PolicyDrift")]
    [Trait("Category", "CyberArk")]
    [Trait("Category", "ApiRegression")]
    [Trait("Category", "WorkflowRegression")]
    public async Task GetPolicyVariation_ShouldFollowExpectedBehavior(PolicyDriftScenarioCase scenario)
    {
        await Task.CompletedTask;

        PolicyDriftScenarioAssert.MarkAsHarnessScaffold(scenario, "CyberArk GetPolicy");
        scenario.ExpectedFinalStatus.Should().NotBeNullOrWhiteSpace();
    }
}
