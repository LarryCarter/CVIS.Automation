using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Models;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Matrix;

public static class PolicyDriftScenarioData
{
    private const string SourceProjectPolicyDriftTestDataPath = "CVIS.Automation.Tests/Projects/PolicyDrift/TestData";
    private const string LocalPolicyDriftTestDataPath = "Integration/PolicyDrift/TestData";

    public static IEnumerable<object[]> CyberArkFailureCases =>
        LoadCyberArkFailureRows("cyberark-failure-cases.json");

    public static IEnumerable<object[]> WorkflowCases =>
        LoadWorkflowRows("policy-drift-workflow-cases.json");

    public static IEnumerable<object[]> CyberArkPlatformCases =>
        LoadScenarioRows("cyberark-platform-cases.json");

    public static IEnumerable<object[]> CyberArkPolicyCases =>
        LoadScenarioRows("cyberark-policy-cases.json");

    public static IEnumerable<object[]> DbFallbackCases =>
        LoadScenarioRows("db-fallback-cases.json");

    public static IEnumerable<object[]> ZipCases =>
        LoadScenarioRows("zip-cases.json");

    public static IEnumerable<object[]> JobCases =>
        LoadScenarioRows("job-cases.json");

    public static IEnumerable<object[]> PolicyProcessingCases =>
        LoadScenarioRows("policy-processing-cases.json");

    public static IEnumerable<object[]> AuditCases =>
        LoadScenarioRows("audit-cases.json");

    public static IEnumerable<object[]> ReportCases =>
        LoadScenarioRows("report-cases.json");

    public static PolicyDriftScenarioCase CreateScenario(
        string name,
        string scenarioType,
        string expectedBehavior,
        string expectedFinalStatus,
        int expectedMinimumRecordCount)
    {
        return new PolicyDriftScenarioCase
        {
            Name = name,
            ScenarioType = scenarioType,
            ExpectedBehavior = expectedBehavior,
            ExpectedFinalStatus = expectedFinalStatus,
            ExpectedMinimumRecordCount = expectedMinimumRecordCount
        };
    }

    public static CyberArkFailureCase CreateCyberArkFailureCase(
        string name,
        int simulatedStatusCode,
        string expectedBehavior)
    {
        return new CyberArkFailureCase(
            name,
            simulatedStatusCode,
            expectedBehavior);
    }

    public static PolicyDriftWorkflowCase CreateWorkflowCase(
        string name,
        string scenarioType,
        string expectedFinalStatus,
        int expectedMinimumDriftCount)
    {
        return new PolicyDriftWorkflowCase(
            name,
            scenarioType,
            expectedFinalStatus,
            expectedMinimumDriftCount);
    }

    private static IEnumerable<object[]> LoadScenarioRows(string fileName)
    {
        foreach (var scenario in LoadPolicyDriftJsonArray<PolicyDriftScenarioCase>(fileName))
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

    private static IEnumerable<object[]> LoadCyberArkFailureRows(string fileName)
    {
        foreach (var scenario in LoadPolicyDriftJsonArray<CyberArkFailureCase>(fileName))
        {
            yield return new object[]
            {
                scenario.Name,
                scenario.SimulatedStatusCode,
                scenario.ExpectedBehavior
            };
        }
    }

    private static IEnumerable<object[]> LoadWorkflowRows(string fileName)
    {
        foreach (var scenario in LoadPolicyDriftJsonArray<PolicyDriftWorkflowCase>(fileName))
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

    private static IEnumerable<T> LoadPolicyDriftJsonArray<T>(string fileName)
    {
        try
        {
            return UnitTestBase.LoadJsonArray<T>(Path.Combine(LocalPolicyDriftTestDataPath, fileName));
        }
        catch (FileNotFoundException)
        {
            return UnitTestBase.LoadJsonArray<T>(Path.Combine(SourceProjectPolicyDriftTestDataPath, fileName));
        }
    }
}
