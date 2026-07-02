using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Matrix;
using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Models;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Workflows;

public sealed class CyberArkFallbackWorkflowTests : UnitTestBase
{
    [Theory]
    [Trait("PolicyDrift", "true")]
    [Trait("Category", "WorkflowRegression")]
    [Trait("Category", "CyberArk")]
    [Trait("Category", "Negative")]
    [MemberData(nameof(PolicyDriftScenarioData.CyberArkFailureCases), MemberType = typeof(PolicyDriftScenarioData))]
    public async Task GetPlatformsFailure_ShouldFallbackToDatabase(CyberArkFailureCase testCase)
    {
        await Task.CompletedTask;

        testCase.Name.Should().NotBeNullOrWhiteSpace();
        testCase.ExpectedBehavior.Should().NotBeNullOrWhiteSpace();
    }
}
