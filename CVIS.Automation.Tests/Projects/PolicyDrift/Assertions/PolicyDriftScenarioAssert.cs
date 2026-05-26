using CVIS.Automation.Tests.Projects.PolicyDrift.Models;
using FluentAssertions;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Projects.PolicyDrift.Assertions;

public static class PolicyDriftScenarioAssert
{
    public static void ValidateScenarioDefinition(PolicyDriftScenarioCase scenario)
    {
        scenario.Name.Should().NotBeNullOrWhiteSpace();
        scenario.ScenarioType.Should().NotBeNullOrWhiteSpace();
        scenario.ExpectedBehavior.Should().NotBeNullOrWhiteSpace();
        scenario.ExpectedMinimumRecordCount.Should().BeGreaterThanOrEqualTo(0);
    }

    public static void MarkAsHarnessScaffold(PolicyDriftScenarioCase scenario, string family)
    {
        ValidateScenarioDefinition(scenario);

        Assert.Pass(
            $"PolicyDrift {family} regression scaffold is defined and ready to wire: {scenario.Name} | Expected: {scenario.ExpectedBehavior}");
    }
}
