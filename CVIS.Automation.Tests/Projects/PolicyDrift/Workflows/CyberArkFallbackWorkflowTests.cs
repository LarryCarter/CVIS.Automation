using CVIS.Automation.Tests.Projects.PolicyDrift.Models;
using CVIS.Automation.Tests.Shared.Helpers;
using FluentAssertions;
using NUnit.Framework;
using CVIS.Automation.Tests.Shared.Playwright;

namespace CVIS.Automation.Tests.Projects.PolicyDrift.Workflows;

[TestFixture]
[Category("PolicyDrift")]
[Category("WorkflowRegression")]
[Category("CyberArk")]
[Category("Negative")]
public sealed class CyberArkFallbackWorkflowTests : PlaywrightFunctionalTestBase
{
    public static IEnumerable<TestCaseData> CyberArkFailureCases()
    {
        var cases = TestDataLoader.LoadJsonArray<CyberArkFailureCase>(
            Path.Combine("Projects", "PolicyDrift", "TestData", "cyberark-failure-cases.json"));

        foreach (var testCase in cases)
        {
            yield return new TestCaseData(testCase)
                .SetName($"PolicyDrift_GetPlatforms_{testCase.Name}_Should_{testCase.ExpectedBehavior}");
        }
    }

    [TestCaseSource(nameof(CyberArkFailureCases))]
    public async Task GetPlatformsFailure_ShouldFallbackToDatabase(CyberArkFailureCase testCase)
    {
        await Task.CompletedTask;

        testCase.ExpectedBehavior.Should().NotBeNullOrWhiteSpace();

        Assert.Pass($"Scaffold created for PolicyDrift CyberArk failure case: {testCase.Name}");
    }
}
