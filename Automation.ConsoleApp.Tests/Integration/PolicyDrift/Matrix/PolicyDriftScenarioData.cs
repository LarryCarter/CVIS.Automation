namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Matrix;

public static class PolicyDriftScenarioData
{
    public static IEnumerable<object[]> CyberArkFailureCases => LoadCyberArkFailureRows("cyberark-failure-cases.json");
    public static IEnumerable<object[]> CyberArkPlatformCases => LoadScenarioRows("cyberark-platform-cases.json");
    public static IEnumerable<object[]> CyberArkPolicyCases => LoadScenarioRows("cyberark-policy-cases.json");
    public static IEnumerable<object[]> DbFallbackCases => LoadScenarioRows("db-fallback-cases.json");
    public static IEnumerable<object[]> ZipCases => LoadScenarioRows("zip-cases.json");
    public static IEnumerable<object[]> JobCases => LoadScenarioRows("job-cases.json");
    public static IEnumerable<object[]> PolicyProcessingCases => LoadScenarioRows("policy-processing-cases.json");
    public static IEnumerable<object[]> AuditCases => LoadScenarioRows("audit-cases.json");
    public static IEnumerable<object[]> ReportCases => LoadScenarioRows("report-cases.json");
    public static IEnumerable<object[]> PolicyDriftWorkflowCases => LoadWorkflowRows("policy-drift-workflow-cases.json");

    private static IEnumerable<object[]> LoadScenarioRows(string fileName)
    {
        foreach (var scenario in UnitTestBase.LoadJsonArray<PolicyDriftScenarioCase>(PolicyDriftTestDataPath(fileName)))
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
        foreach (var scenario in UnitTestBase.LoadJsonArray<PolicyDriftWorkflowCase>(PolicyDriftTestDataPath(fileName)))
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
        foreach (var scenario in UnitTestBase.LoadJsonArray<CyberArkFailureCase>(PolicyDriftTestDataPath(fileName)))
        {
            yield return new object[]
            {
                scenario.Name,
                scenario.SimulatedStatusCode,
                scenario.ExpectedBehavior
            };
        }
    }

    private static string PolicyDriftTestDataPath(string fileName)
    {
        return Path.Combine("Integration", "PolicyDrift", "TestData", fileName);
    }
}
