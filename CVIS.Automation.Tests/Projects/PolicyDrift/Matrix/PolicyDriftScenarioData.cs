using CVIS.Automation.Tests.Projects.PolicyDrift.Models;
using CVIS.Playwright.Automation.Shared.Helpers;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Projects.PolicyDrift.Matrix;

public static class PolicyDriftScenarioData
{
    private static IEnumerable<TestCaseData> Load(string fileName, string prefix)
    {
        var cases = TestDataLoader.LoadJsonArray<PolicyDriftScenarioCase>(
            Path.Combine("Projects", "PolicyDrift", "TestData", fileName));

        foreach (var testCase in cases)
        {
            yield return new TestCaseData(testCase)
                .SetName($"{prefix}_{testCase.Name}");
        }
    }

    public static IEnumerable<TestCaseData> CyberArkPlatformCases() =>
        Load("cyberark-platform-cases.json", "PolicyDrift_CyberArkPlatform");

    public static IEnumerable<TestCaseData> CyberArkPolicyCases() =>
        Load("cyberark-policy-cases.json", "PolicyDrift_CyberArkPolicy");

    public static IEnumerable<TestCaseData> DbFallbackCases() =>
        Load("db-fallback-cases.json", "PolicyDrift_DbFallback");

    public static IEnumerable<TestCaseData> ZipCases() =>
        Load("zip-cases.json", "PolicyDrift_Zip");

    public static IEnumerable<TestCaseData> JobCases() =>
        Load("job-cases.json", "PolicyDrift_Job");

    public static IEnumerable<TestCaseData> PolicyProcessingCases() =>
        Load("policy-processing-cases.json", "PolicyDrift_Processing");

    public static IEnumerable<TestCaseData> AuditCases() =>
        Load("audit-cases.json", "PolicyDrift_Audit");

    public static IEnumerable<TestCaseData> ReportCases() =>
        Load("report-cases.json", "PolicyDrift_Report");
}
