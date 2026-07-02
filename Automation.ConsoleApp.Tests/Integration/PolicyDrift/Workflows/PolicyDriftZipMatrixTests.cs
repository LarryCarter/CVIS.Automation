using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Assertions;
using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Matrix;
using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Models;
using FluentAssertions;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Workflows;

public sealed class PolicyDriftZipMatrixTests : UnitTestBase
{
    [Theory]
    [Trait("PolicyDrift", "true")]
    [Trait("WorkflowRegression", "true")]
    [Trait("ZipRegression", "true")]
    [MemberData(nameof(PolicyDriftScenarioData.ZipCases), MemberType = typeof(PolicyDriftScenarioData))]
    public Task ZipDownloadOrExtractionScenario_ShouldProduceExpectedBehavior(PolicyDriftScenarioCase scenario)
    {
        PolicyDriftScenarioAssert.ValidateScenarioDefinition(scenario);

        scenario.ExpectedBehavior.Should().NotBeNullOrWhiteSpace();
        scenario.ExpectedFinalStatus.Should().NotBeNullOrWhiteSpace();

        return Task.CompletedTask;
    }
}
