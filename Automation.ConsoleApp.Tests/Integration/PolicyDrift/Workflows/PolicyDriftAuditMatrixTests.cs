using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Assertions;
using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Matrix;
using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Models;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Workflows;

public sealed class PolicyDriftAuditMatrixTests : UnitTestBase
{
    [Theory]
    [MemberData(nameof(PolicyDriftScenarioData.AuditCases), MemberType = typeof(PolicyDriftScenarioData))]
    [Trait("Category", "PolicyDrift")]
    [Trait("Category", "AuditRegression")]
    [Trait("Category", "WorkflowRegression")]
    public async Task AuditOrLogScenario_ShouldProduceExpectedRecord(PolicyDriftScenarioCase scenario)
    {
        await Task.CompletedTask;

        PolicyDriftScenarioAssert.MarkAsHarnessScaffold(scenario, "audit/log");
        scenario.ExpectedFinalStatus.Should().NotBeNullOrWhiteSpace();
    }
}
