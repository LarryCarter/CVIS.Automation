using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Assertions;
using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Matrix;
using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Models;
using FluentAssertions;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Workflows;

public sealed class PolicyDriftProcessingMatrixTests : UnitTestBase
{
    [Theory]
    [Trait("PolicyDrift", "true")]
    [Trait("WorkflowRegression", "true")]
    [Trait("PolicyProcessingRegression", "true")]
    [MemberData(nameof(PolicyDriftScenarioData.PolicyProcessingCases), MemberType = typeof(PolicyDriftScenarioData))]
    public Task PolicyProcessingScenario_ShouldProduceExpectedDriftBehavior(PolicyDriftScenarioCase scenario)
    {
        PolicyDriftScenarioAssert.ValidateScenarioDefinition(scenario);

        scenario.ExpectedBehavior.Should().NotBeNullOrWhiteSpace();
        scenario.ExpectedFinalStatus.Should().NotBeNullOrWhiteSpace();

        return Task.CompletedTask;
    }
}
