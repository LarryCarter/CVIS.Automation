using CVIS.Automation.Tests.Projects.PolicyDrift.Assertions;
using CVIS.Automation.Tests.Projects.PolicyDrift.Matrix;
using CVIS.Automation.Tests.Projects.PolicyDrift.Models;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Projects.PolicyDrift.Workflows;

[TestFixture]
[Category("PolicyDrift")]
[Category("PolicyProcessingRegression")]
[Category("WorkflowRegression")]
public sealed class PolicyDriftProcessingMatrixTests
{
    [TestCaseSource(typeof(PolicyDriftScenarioData), nameof(PolicyDriftScenarioData.PolicyProcessingCases))]
    public void PolicyProcessingScenario_ShouldProduceExpectedDriftBehavior(PolicyDriftScenarioCase scenario)
    {
        PolicyDriftScenarioAssert.MarkAsHarnessScaffold(scenario, "policy processing");
    }
}
