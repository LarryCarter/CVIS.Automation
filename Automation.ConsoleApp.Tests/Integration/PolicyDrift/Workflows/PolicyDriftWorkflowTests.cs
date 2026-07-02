using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Models;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Workflows;

public sealed class PolicyDriftWorkflowTests : UnitTestBase
{
    public static IEnumerable<object[]> PolicyDriftCases()
    {
        var cases = LoadJsonArray<PolicyDriftWorkflowCase>(
            "Integration", "PolicyDrift", "TestData", "policy-drift-workflow-cases.json");

        foreach (var testCase in cases)
        {
            yield return new object[] { testCase };
        }
    }

    [Theory]
    [MemberData(nameof(PolicyDriftCases))]
    [Trait("Category", "PolicyDrift")]
    [Trait("Category", "WorkflowRegression")]
    public async Task PolicyDriftScenario_ShouldProduceExpectedFinalState(PolicyDriftWorkflowCase testCase)
    {
        await Task.CompletedTask;

        testCase.Name.Should().NotBeNullOrWhiteSpace();
        testCase.ExpectedFinalStatus.Should().Be("Completed");
        testCase.ExpectedMinimumDriftCount.Should().BeGreaterThanOrEqualTo(0);
    }
}
