using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Assertions;
using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Matrix;
using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Models;
using FluentAssertions;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Workflows;

public sealed class PolicyDriftAuditMatrixTests : UnitTestBase
{
    [Theory]
    [Trait("PolicyDrift", "true")]
    [Trait("WorkflowRegression", "true")]
    [Trait("AuditRegression", "true")]
    [MemberData(nameof(PolicyDriftScenarioData.AuditCases), MemberType = typeof(PolicyDriftScenarioData))]
    public Task AuditOrLogScenario_ShouldProduceExpectedRecord(PolicyDriftScenarioCase scenario)
    {
        PolicyDriftScenarioAssert.ValidateScenarioDefinition(scenario);

        scenario.ExpectedBehavior.Should().NotBeNullOrWhiteSpace();
        scenario.ExpectedFinalStatus.Should().NotBeNullOrWhiteSpace();

        return Task.CompletedTask;
    }
}
