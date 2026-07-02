using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Models;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Matrix;

public static class PolicyDriftScenarioData
{
    public static IEnumerable<object[]> CyberArkFailureCases =>
        LoadCyberArkFailureCases("cyberark-failure-cases.json");

    public static IEnumerable<object[]> PolicyDriftWorkflowCases =>
        LoadWorkflowCases("policy-drift-workflow-cases.json");

    public static IEnumerable<object[]> CyberArkPlatformCases =>
        LoadScenarioCases("cyberark-platform-cases.json");

    public static IEnumerable<object[]> CyberArkPolicyCases =>
        LoadScenarioCases("cyberark-policy-cases.json");

    public static IEnumerable<object[]> DbFallbackCases =>
        LoadScenarioCases("db-fallback-cases.json");

    public static IEnumerable<object[]> ZipCases =>
        LoadScenarioCases("zip-cases.json");

    public static IEnumerable<object[]> JobCases =>
        LoadScenarioCases("job-cases.json");

    public static IEnumerable<object[]> PolicyProcessingCases =>
        LoadScenarioCases("policy-processing-cases.json");

    public static IEnumerable<object[]> AuditCases =>
        LoadScenarioCases("audit-cases.json");

    public static IEnumerable<object[]> ReportCases =>
        LoadScenarioCases("report-cases.json");

    private static IEnumerable<object[]> LoadScenarioCases(string fileName)
    {
        return UnitTestBase
            .LoadJsonArray<PolicyDriftScenarioCase>(Path.Combine("Projects", "PolicyDrift", "TestData", fileName))
            .Select(static scenario => new object[] { scenario });
    }

    private static IEnumerable<object[]> LoadWorkflowCases(string fileName)
    {
        return UnitTestBase
            .LoadJsonArray<PolicyDriftWorkflowCase>(Path.Combine("Projects", "PolicyDrift", "TestData", fileName))
            .Select(static scenario => new object[] { scenario });
    }

    private static IEnumerable<object[]> LoadCyberArkFailureCases(string fileName)
    {
        return UnitTestBase
            .LoadJsonArray<CyberArkFailureCase>(Path.Combine("Projects", "PolicyDrift", "TestData", fileName))
            .Select(static scenario => new object[] { scenario });
    }
}
