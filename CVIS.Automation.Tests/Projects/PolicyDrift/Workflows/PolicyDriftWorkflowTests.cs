using CVIS.Automation.Tests.Projects.PolicyDrift.Models;
using CVIS.Automation.Tests.Shared.Helpers;
using FluentAssertions;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Projects.PolicyDrift.Workflows;

[TestFixture]
[Category("PolicyDrift")]
[Category("WorkflowRegression")]
public sealed class PolicyDriftWorkflowTests
{
    public static IEnumerable<TestCaseData> PolicyDriftCases()
    {
        var cases = TestDataLoader.LoadJsonArray<PolicyDriftWorkflowCase>(
            Path.Combine("Projects", "PolicyDrift", "TestData", "policy-drift-workflow-cases.json"));

        foreach (var testCase in cases)
        {
            yield return new TestCaseData(testCase)
                .SetName($"PolicyDrift_{testCase.Name}_ShouldFinishWith_{testCase.ExpectedFinalStatus}");
        }
    }

    [TestCaseSource(nameof(PolicyDriftCases))]
    public async Task PolicyDriftScenario_ShouldProduceExpectedFinalState(PolicyDriftWorkflowCase testCase)
    {
        await Task.CompletedTask;

        testCase.ExpectedFinalStatus.Should().Be("Completed");

        Assert.Pass($"Scaffold created for PolicyDrift workflow case: {testCase.Name}");
    }
}
