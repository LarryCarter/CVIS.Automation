using CVIS.Automation.Tests.Projects.PolicyDrift.Assertions;
using CVIS.Automation.Tests.Projects.PolicyDrift.Matrix;
using CVIS.Automation.Tests.Projects.PolicyDrift.Models;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Projects.PolicyDrift.Workflows;

[TestFixture]
[Category("PolicyDrift")]
[Category("JobRegression")]
[Category("WorkflowRegression")]
public sealed class PolicyDriftJobMatrixTests
{
    [TestCaseSource(typeof(PolicyDriftScenarioData), nameof(PolicyDriftScenarioData.JobCases))]
    public void ScheduledJobScenario_ShouldProduceExpectedBehavior(PolicyDriftScenarioCase scenario)
    {
        PolicyDriftScenarioAssert.MarkAsHarnessScaffold(scenario, "scheduled job");
    }
}
