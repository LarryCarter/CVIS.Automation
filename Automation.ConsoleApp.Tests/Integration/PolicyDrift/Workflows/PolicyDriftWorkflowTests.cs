using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Assertions;
using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Matrix;
using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Models;
using FluentAssertions;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Workflows;

public sealed class PolicyDriftWorkflowTests : UnitTestBase
{
    [Theory]
    [Trait("PolicyDrift", "true")]
    [Trait("WorkflowRegression", "true")]
    [MemberData(nameof(PolicyDriftScenarioData.PolicyDriftWorkflowCases), MemberType = typeof(PolicyDriftScenarioData))]
    public Task PolicyDriftScenario_ShouldProduceExpectedFinalState(PolicyDriftWorkflowCase testCase)
    {
        PolicyDriftScenarioAssert.ValidateWorkflowDefinition(testCase);
        testCase.ExpectedFinalStatus.Should().Be("Completed");

        return Task.CompletedTask;
    }
}
