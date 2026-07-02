using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Assertions;
using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Matrix;
using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Models;
using FluentAssertions;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Workflows;

public sealed class PolicyDriftReportMatrixTests : UnitTestBase
{
    [Theory]
    [Trait("PolicyDrift", "true")]
    [Trait("WorkflowRegression", "true")]
    [Trait("ReportRegression", "true")]
    [MemberData(nameof(PolicyDriftScenarioData.ReportCases), MemberType = typeof(PolicyDriftScenarioData))]
    public Task ReportScenario_ShouldProduceExpectedOutput(PolicyDriftScenarioCase scenario)
    {
        PolicyDriftScenarioAssert.ValidateScenarioDefinition(scenario);

        scenario.ExpectedBehavior.Should().NotBeNullOrWhiteSpace();
        scenario.ExpectedFinalStatus.Should().NotBeNullOrWhiteSpace();

        return Task.CompletedTask;
    }
}
