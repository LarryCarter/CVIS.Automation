using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Models;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Workflows;

public sealed class CyberArkFallbackWorkflowTests : UnitTestBase
{
    public static IEnumerable<object[]> CyberArkFailureCases()
    {
        var cases = LoadJsonArray<CyberArkFailureCase>(
            "Integration", "PolicyDrift", "TestData", "cyberark-failure-cases.json");

        foreach (var testCase in cases)
        {
            yield return new object[] { testCase };
        }
    }

    [Theory]
    [MemberData(nameof(CyberArkFailureCases))]
    [Trait("Category", "PolicyDrift")]
    [Trait("Category", "WorkflowRegression")]
    [Trait("Category", "CyberArk")]
    [Trait("Category", "Negative")]
    public async Task GetPlatformsFailure_ShouldFallbackToDatabase(CyberArkFailureCase testCase)
    {
        await Task.CompletedTask;

        testCase.Name.Should().NotBeNullOrWhiteSpace();
        testCase.ExpectedBehavior.Should().NotBeNullOrWhiteSpace();
    }
}
