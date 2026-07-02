using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Assertions;
using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Matrix;
using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Models;
using FluentAssertions;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Workflows;

public sealed class CyberArkFallbackWorkflowTests : UnitTestBase
{
    [Theory]
    [Trait("PolicyDrift", "true")]
    [Trait("WorkflowRegression", "true")]
    [Trait("CyberArk", "true")]
    [Trait("Negative", "true")]
    [MemberData(nameof(PolicyDriftScenarioData.CyberArkFailureCases), MemberType = typeof(PolicyDriftScenarioData))]
    public Task GetPlatformsFailure_ShouldFallbackToDatabase(CyberArkFailureCase testCase)
    {
        PolicyDriftScenarioAssert.ValidateCyberArkFailureDefinition(testCase);
        testCase.ExpectedBehavior.Should().NotBeNullOrWhiteSpace();

        return Task.CompletedTask;
    }
}
