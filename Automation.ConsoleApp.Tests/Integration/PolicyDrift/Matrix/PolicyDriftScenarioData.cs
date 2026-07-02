using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Models;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Matrix;

public static class PolicyDriftScenarioData
{
    public static IEnumerable<object[]> CyberArkPlatformCases => LoadScenarioRows("cyberark-platform-cases.json");
    public static IEnumerable<object[]> CyberArkPolicyCases => LoadScenarioRows("cyberark-policy-cases.json");
    public static IEnumerable<object[]> DbFallbackCases => LoadScenarioRows("db-fallback-cases.json");
    public static IEnumerable<object[]> ZipCases => LoadScenarioRows("zip-cases.json");
    public static IEnumerable<object[]> JobCases => LoadScenarioRows("job-cases.json");
    public static IEnumerable<object[]> PolicyProcessingCases => LoadScenarioRows("policy-processing-cases.json");
    public static IEnumerable<object[]> AuditCases => LoadScenarioRows("audit-cases.json");
    public static IEnumerable<object[]> ReportCases => LoadScenarioRows("report-cases.json");

    public static IEnumerable<object[]> WorkflowCases => LoadWorkflowRows("policy-drift-workflow-cases.json");
    public static IEnumerable<object[]> PolicyDriftWorkflowCases => WorkflowCases;

    public static IEnumerable<object[]> CyberArkFailureCases => LoadCyberArkFailureRows("cyberark-failure-cases.json");

    private static IEnumerable<object[]> LoadScenarioRows(string fileName)
    {
        foreach (var scenario in UnitTestBase.LoadJsonArray<PolicyDriftScenarioCase>(Path.Combine("Integration", "PolicyDrift", "TestData", fileName)))
        {
            yield return new object[]
            {
                scenario.Name,
                scenario.ScenarioType,
                scenario.ExpectedBehavior,
                scenario.ExpectedFinalStatus,
                scenario.ExpectedMinimumRecordCount
            };
        }
    }

    private static IEnumerable<object[]> LoadWorkflowRows(string fileName)
    {
        foreach (var scenario in UnitTestBase.LoadJsonArray<PolicyDriftWorkflowCase>(Path.Combine("Integration", "PolicyDrift", "TestData", fileName)))
        {
            yield return new object[]
            {
                scenario.Name,
                scenario.ScenarioType,
                scenario.ExpectedFinalStatus,
                scenario.ExpectedMinimumDriftCount
            };
        }
    }

    private static IEnumerable<object[]> LoadCyberArkFailureRows(string fileName)
    {
        foreach (var scenario in UnitTestBase.LoadJsonArray<CyberArkFailureCase>(Path.Combine("Integration", "PolicyDrift", "TestData", fileName)))
        {
            yield return new object[]
            {
                scenario.Name,
                scenario.SimulatedStatusCode,
                scenario.ExpectedBehavior
            };
        }
    }
}
