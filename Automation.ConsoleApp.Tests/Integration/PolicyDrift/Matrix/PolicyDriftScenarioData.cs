using Automation.ConsoleApp.Tests.Integration.PolicyDrift.Models;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Matrix;

public static class PolicyDriftScenarioData
{
    private static IEnumerable<object[]> Load(string fileName)
    {
        var cases = UnitTestData.LoadJsonArray<PolicyDriftScenarioCase>(
            "Integration", "PolicyDrift", "TestData", fileName);

        foreach (var testCase in cases)
        {
            yield return new object[] { testCase };
        }
    }

    public static IEnumerable<object[]> CyberArkPlatformCases() => Load("cyberark-platform-cases.json");
    public static IEnumerable<object[]> CyberArkPolicyCases() => Load("cyberark-policy-cases.json");
    public static IEnumerable<object[]> DbFallbackCases() => Load("db-fallback-cases.json");
    public static IEnumerable<object[]> ZipCases() => Load("zip-cases.json");
    public static IEnumerable<object[]> JobCases() => Load("job-cases.json");
    public static IEnumerable<object[]> PolicyProcessingCases() => Load("policy-processing-cases.json");
    public static IEnumerable<object[]> AuditCases() => Load("audit-cases.json");
    public static IEnumerable<object[]> ReportCases() => Load("report-cases.json");
}
