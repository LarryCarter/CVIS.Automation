using CVIS.Automation.Tests.Projects.PolicyDrift.Assertions;
using CVIS.Automation.Tests.Projects.PolicyDrift.Matrix;
using CVIS.Automation.Tests.Projects.PolicyDrift.Models;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Projects.PolicyDrift.Workflows;

[TestFixture]
[Category("PolicyDrift")]
[Category("DatabaseRegression")]
[Category("WorkflowRegression")]
public sealed class PolicyDriftDbFallbackMatrixTests
{
    [TestCaseSource(typeof(PolicyDriftScenarioData), nameof(PolicyDriftScenarioData.DbFallbackCases))]
    public void DatabaseFallbackScenario_ShouldProduceExpectedBehavior(PolicyDriftScenarioCase scenario)
    {
        PolicyDriftScenarioAssert.MarkAsHarnessScaffold(scenario, "DB fallback");
    }
}
