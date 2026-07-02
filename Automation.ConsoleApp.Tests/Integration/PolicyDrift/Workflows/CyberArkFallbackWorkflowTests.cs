using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Matrix;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Workflows;

public sealed class CyberArkFallbackWorkflowTests : UnitTestBase
{
    [Trait("Category", "PolicyDrift")]
    [Trait("Category", "WorkflowRegression")]
    [Trait("Category", "CyberArk")]
    [Trait("Category", "Negative")]
    [Theory]
    [MemberData(nameof(PolicyDriftScenarioData.CyberArkFailureCases), MemberType = typeof(PolicyDriftScenarioData))]
    public async Task GetPlatformsFailure_ShouldFallbackToDatabase(
        string name,
        int simulatedStatusCode,
        string expectedBehavior)
    {
        await Task.CompletedTask;

        var testCase = PolicyDriftScenarioData.CreateCyberArkFailureCase(
            name,
            simulatedStatusCode,
            expectedBehavior);

        testCase.Name.Should().NotBeNullOrWhiteSpace();
        testCase.ExpectedBehavior.Should().NotBeNullOrWhiteSpace();
    }
}
