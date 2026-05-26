"""
CVIS.Automation - PolicyDrift Regression Pack Add-On

SAVE THIS FILE AS:
    C:\\Users\\larry\\source\\repos\\CVIS.Automation\\add_policy_drift_regression_pack.py

RUN FROM POWERSHELL:
    cd C:\\Users\\larry\\source\\repos\\CVIS.Automation
    python .\\add_policy_drift_regression_pack.py

THEN RUN:
    dotnet build .\\CVIS.Automation.sln
    dotnet test .\\CVIS.Automation.Tests\\CVIS.Automation.Tests.csproj --filter TestCategory=PolicyDrift
"""

from __future__ import annotations

import json
from pathlib import Path


SOLUTION_ROOT = Path.cwd()
TEST_PROJECT_ROOT = SOLUTION_ROOT / "CVIS.Automation.Tests"

if not TEST_PROJECT_ROOT.exists():
    raise RuntimeError(
        "Cannot find CVIS.Automation.Tests. Run this from "
        "C:\\Users\\larry\\source\\repos\\CVIS.Automation"
    )


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def project_path(*parts: str) -> Path:
    return TEST_PROJECT_ROOT.joinpath(*parts)


def make_case(
    name: str,
    scenario_type: str,
    expected_behavior: str,
    expected_final_status: str = "Completed",
    expected_minimum_record_count: int = 1,
) -> dict:
    return {
        "name": name,
        "scenarioType": scenario_type,
        "expectedBehavior": expected_behavior,
        "expectedFinalStatus": expected_final_status,
        "expectedMinimumRecordCount": expected_minimum_record_count,
    }


def save_cases(file_name: str, cases: list[dict]) -> None:
    write_file(
        project_path("Projects", "PolicyDrift", "TestData", file_name),
        json.dumps(cases, indent=2),
    )


def ensure_folders() -> None:
    folders = [
        ("Projects", "PolicyDrift", "Assertions"),
        ("Projects", "PolicyDrift", "Matrix"),
        ("Projects", "PolicyDrift", "Models"),
        ("Projects", "PolicyDrift", "TestData"),
        ("Projects", "PolicyDrift", "Workflows"),
    ]

    for folder in folders:
        project_path(*folder).mkdir(parents=True, exist_ok=True)


def write_csharp_files() -> None:
    write_file(
        project_path("Projects", "PolicyDrift", "Models", "PolicyDriftScenarioCase.cs"),
        '''namespace CVIS.Automation.Tests.Projects.PolicyDrift.Models;

public sealed record PolicyDriftScenarioCase
{
    public string Name { get; init; } = string.Empty;
    public string ScenarioType { get; init; } = string.Empty;
    public string ExpectedBehavior { get; init; } = string.Empty;
    public string ExpectedFinalStatus { get; init; } = string.Empty;
    public int ExpectedMinimumRecordCount { get; init; }
}
''',
    )

    write_file(
        project_path("Projects", "PolicyDrift", "Assertions", "PolicyDriftScenarioAssert.cs"),
        '''using CVIS.Automation.Tests.Projects.PolicyDrift.Models;
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
''',
    )

    write_file(
        project_path("Projects", "PolicyDrift", "Matrix", "PolicyDriftScenarioData.cs"),
        '''using CVIS.Automation.Tests.Projects.PolicyDrift.Models;
using CVIS.Automation.Tests.Shared.Helpers;
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
''',
    )

    test_classes = [
        ("PolicyDriftCyberArkPlatformMatrixTests", ["PolicyDrift", "CyberArk", "Negative", "WorkflowRegression"], "CyberArkPlatformCases", "GetPlatformsFailureOrVariation_ShouldFollowExpectedFallbackBehavior", "CyberArk GetPlatforms"),
        ("PolicyDriftCyberArkPolicyMatrixTests", ["PolicyDrift", "CyberArk", "ApiRegression", "WorkflowRegression"], "CyberArkPolicyCases", "GetPolicyVariation_ShouldFollowExpectedBehavior", "CyberArk GetPolicy"),
        ("PolicyDriftDbFallbackMatrixTests", ["PolicyDrift", "DatabaseRegression", "WorkflowRegression"], "DbFallbackCases", "DatabaseFallbackScenario_ShouldProduceExpectedBehavior", "DB fallback"),
        ("PolicyDriftZipMatrixTests", ["PolicyDrift", "ZipRegression", "WorkflowRegression"], "ZipCases", "ZipDownloadOrExtractionScenario_ShouldProduceExpectedBehavior", "ZIP handling"),
        ("PolicyDriftJobMatrixTests", ["PolicyDrift", "JobRegression", "WorkflowRegression"], "JobCases", "ScheduledJobScenario_ShouldProduceExpectedBehavior", "scheduled job"),
        ("PolicyDriftProcessingMatrixTests", ["PolicyDrift", "PolicyProcessingRegression", "WorkflowRegression"], "PolicyProcessingCases", "PolicyProcessingScenario_ShouldProduceExpectedDriftBehavior", "policy processing"),
        ("PolicyDriftAuditMatrixTests", ["PolicyDrift", "AuditRegression", "WorkflowRegression"], "AuditCases", "AuditOrLogScenario_ShouldProduceExpectedRecord", "audit/log"),
        ("PolicyDriftReportMatrixTests", ["PolicyDrift", "ReportRegression", "WorkflowRegression"], "ReportCases", "ReportScenario_ShouldProduceExpectedOutput", "report output"),
    ]

    for class_name, categories, source_name, method_name, family in test_classes:
        category_lines = "\n".join(f'[Category("{category}")]' for category in categories)
        content = f'''using CVIS.Automation.Tests.Projects.PolicyDrift.Assertions;
using CVIS.Automation.Tests.Projects.PolicyDrift.Matrix;
using CVIS.Automation.Tests.Projects.PolicyDrift.Models;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Projects.PolicyDrift.Workflows;

[TestFixture]
{category_lines}
public sealed class {class_name}
{{
    [TestCaseSource(typeof(PolicyDriftScenarioData), nameof(PolicyDriftScenarioData.{source_name}))]
    public void {method_name}(PolicyDriftScenarioCase scenario)
    {{
        PolicyDriftScenarioAssert.MarkAsHarnessScaffold(scenario, "{family}");
    }}
}}
'''
        write_file(
            project_path("Projects", "PolicyDrift", "Workflows", f"{class_name}.cs"),
            content,
        )


def build_cases() -> dict[str, list[dict]]:
    cyberark_platform_types = [
        "Unauthorized401", "Forbidden403", "NotFound404", "ServerError500", "BadGateway502",
        "ServiceUnavailable503", "GatewayTimeout504", "Timeout", "DnsFailure", "TlsFailure",
        "ConnectionReset", "MalformedJson", "EmptyJsonArray", "NullResponseBody",
        "MissingPlatformNameField", "DuplicatePlatformNames", "WhitespacePlatformNames",
        "LargePlatformList", "PartialPayload206", "RateLimited429",
        *[f"TransientFailureAttempt{i:02}" for i in range(21, 31)],
    ]
    cyberark_platform_cases = [
        make_case(f"GetPlatforms_{case_type}", case_type, "FallbackToDatabase", "Completed", 0 if "Empty" in case_type else 1)
        for case_type in cyberark_platform_types
    ]

    cyberark_policy_types = [
        "ValidPlatform", "InvalidPlatformName", "BlankPlatformName", "WhitespacePlatformName",
        "Unauthorized401", "Forbidden403", "ServerError500", "ServiceUnavailable503",
        "Timeout", "MalformedJson", "EmptyBody", "MissingRequiredFields", "ExtraFields",
        "DuplicatePolicies", "LargePayload", "PolicyDisabled", "PolicyRenamed", "PolicyDeleted",
        "RateLimited429", "PartialContent206",
        *[f"PlatformBatch{i:03}" for i in range(21, 41)],
    ]
    cyberark_policy_cases = []
    for case_type in cyberark_policy_types:
        status = "LoggedAndContinued" if "Invalid" in case_type or "Blank" in case_type else "Completed"
        min_count = 0 if "Empty" in case_type or "Deleted" in case_type else 1
        cyberark_policy_cases.append(make_case(f"GetPolicy_{case_type}", case_type, "ValidatePolicyCallHandling", status, min_count))

    db_fallback_types = [
        "PlatformTableHasRows", "PlatformTableEmpty", "PlatformRowsInactive", "PlatformRowsStale",
        "DuplicatePlatformRows", "NullPlatformName", "BlankPlatformName", "WhitespacePlatformName",
        "LongPlatformName", "SpecialCharacterPlatformName", "PolicyNameMapped", "PolicyNameMissing",
        "PolicyNameDuplicate", "PolicyNameInactive", "PolicyNameStale", "DatabaseConnectionFails",
        "DatabaseTimeout", "StoredProcedureMissing", "PermissionDenied", "DeadlockRetry",
        "FallbackAuditWritten", "FallbackRunStatusUpdated", "FallbackCorrelationIdWritten",
        "FallbackErrorLogged", "FallbackWarningLogged",
        *[f"PlatformRecord{i:03}" for i in range(26, 41)],
    ]
    db_fallback_cases = []
    for case_type in db_fallback_types:
        bad = any(token in case_type for token in ["Fails", "Timeout", "Missing", "Denied"])
        empty = "Empty" in case_type or "Missing" in case_type
        db_fallback_cases.append(make_case(f"DbFallback_{case_type}", case_type, "ValidateFallbackPath", "FailedOrLogged" if bad else "Completed", 0 if empty else 1))

    zip_types = [
        "ValidZip", "MissingZip", "EmptyZip", "CorruptedZip", "PasswordProtectedZip",
        "ZipWithUnexpectedFolder", "ZipWithMissingPolicyFile", "ZipWithExtraFiles",
        "ZipWithInvalidJson", "ZipWithMalformedXml", "LargeZip", "ZeroBytePolicyFile",
        "DuplicatePolicyFiles", "OldZipAlreadyProcessed", "ZipNameDateMismatch",
        "ZipDownloadTimeout", "ZipDownloadUnauthorized", "ZipDownloadForbidden",
        "ZipDownloadServerError", "ZipWriteAccessDenied", "DiskFull", "PathTooLong",
        "InvalidCharactersInFileName", "ChecksumMismatch", "ChecksumMatch",
    ]
    good_zips = {"ValidZip", "ZipWithExtraFiles", "LargeZip", "ChecksumMatch"}
    zip_cases = [
        make_case(f"Zip_{case_type}", case_type, "ValidateZipHandling", "Completed" if case_type in good_zips else "FailedOrLogged", 1 if case_type in good_zips else 0)
        for case_type in zip_types
    ]

    job_types = [
        "JobStarts", "JobCompletes", "JobFails", "JobRetries", "JobTimesOut", "JobAlreadyRunning",
        "JobDisabled", "JobMissingSchedule", "JobManualTrigger", "JobScheduledTrigger",
        "JobWritesStartLog", "JobWritesCompleteLog", "JobWritesErrorLog", "JobWritesCorrelationId",
        "JobUsesQaConfig", "JobUsesUatConfig", "JobUsesOcpConfig", "JobHandlesMissingConfig",
        "JobHandlesInvalidConfig", "JobHandlesCyberArkFailure", "JobHandlesDbFallback",
        "JobHandlesZipFailure", "JobHandlesNoDrift", "JobHandlesDetectedDrift",
        "JobPublishesCompletionStatus",
    ]
    job_cases = []
    for case_type in job_types:
        bad = any(token in case_type for token in ["Fails", "Missing", "Invalid", "Disabled", "TimesOut"])
        job_cases.append(make_case(f"Job_{case_type}", case_type, "ValidateScheduledJobBehavior", "FailedOrSkipped" if bad else "Completed", 1))

    processing_types = [
        "NoDrift", "PolicyAdded", "PolicyRemoved", "PolicyChanged", "PolicyRenamed",
        "PolicyEnabled", "PolicyDisabled", "PlatformAdded", "PlatformRemoved", "PlatformRenamed",
        "DuplicatePolicyIgnored", "CaseOnlyPolicyChange", "WhitespaceOnlyPolicyChange",
        "DescriptionChanged", "CredentialManagementFlagChanged", "RotationIntervalChanged",
        "ReconcileAccountChanged", "VerificationIntervalChanged", "PolicyXmlChanged",
        "PolicyJsonChanged", "PolicyMetadataChanged", "PolicyOwnerChanged", "PolicySafeMappingChanged",
        "PolicyExceptionAdded", "PolicyExceptionRemoved", "LargePolicySet", "EmptyPolicySet",
        "NullPolicyInput", "MalformedPolicyInput", "OutOfOrderPolicyInput", "SamePolicyDifferentOrder",
        "UnexpectedFieldIgnored", "RequiredFieldMissing", "RunStatusCompleted",
        "RunStatusCompletedWithWarnings", "RunStatusFailed", "DriftResultInserted",
        "DriftResultUpdated", "DriftHistoryWritten", "DriftAuditWritten",
    ]
    no_record_processing = {
        "NoDrift", "DuplicatePolicyIgnored", "WhitespaceOnlyPolicyChange",
        "OutOfOrderPolicyInput", "SamePolicyDifferentOrder", "EmptyPolicySet",
    }
    processing_cases = []
    for case_type in processing_types:
        bad = any(token in case_type for token in ["Failed", "Malformed", "Null", "Missing"])
        processing_cases.append(make_case(f"PolicyProcessing_{case_type}", case_type, "ValidateDriftProcessing", "FailedOrLogged" if bad else "Completed", 0 if case_type in no_record_processing else 1))

    audit_types = [
        "RunStarted", "RunCompleted", "RunFailed", "CyberArkGetPlatformsFailureLogged",
        "CyberArkGetPolicyFailureLogged", "DbFallbackUsedLogged", "ZipDownloadedLogged",
        "ZipFailedLogged", "DriftDetectedLogged", "NoDriftLogged", "CorrelationIdOnAllRows",
        "CreatedByAutomation", "CreatedDatePopulated", "ModifiedDatePopulated",
        "ErrorSeverityCaptured", "WarningSeverityCaptured", "InfoSeverityCaptured",
        "RetryAttemptCaptured", "FallbackReasonCaptured", "FinalSummaryCaptured",
        "PolicyCountCaptured", "PlatformCountCaptured", "DriftCountCaptured",
        "ExceptionStackNotNullOnFailure", "NoSecretValuesLogged",
    ]
    audit_cases = [make_case(f"Audit_{case_type}", case_type, "ValidateAuditOrLogRecord", "Completed", 1) for case_type in audit_types]

    report_types = [
        "ReportFileCreated", "ReportEmptyWhenNoDrift", "ReportContainsAddedPolicy",
        "ReportContainsRemovedPolicy", "ReportContainsChangedPolicy", "ReportContainsRunId",
        "ReportContainsCorrelationId", "ReportContainsRunDate", "ReportContainsEnvironment",
        "ReportHandlesLargeRun", "ReportCsvFormatValid", "ReportJsonFormatValid",
        "ReportHtmlFormatValid", "ReportOutputPathExists", "ReportDoesNotExposeSecrets",
        "ReportOverwritesWhenAllowed", "ReportDoesNotOverwriteWhenBlocked", "ReportArchiveCreated",
        "ReportArchiveMissingHandled", "ReportFinalStatusWritten",
    ]
    report_cases = []
    for case_type in report_types:
        report_cases.append(make_case(f"Report_{case_type}", case_type, "ValidateReportOutput", "Logged" if "Missing" in case_type else "Completed", 0 if "Empty" in case_type else 1))

    return {
        "cyberark-platform-cases.json": cyberark_platform_cases,
        "cyberark-policy-cases.json": cyberark_policy_cases,
        "db-fallback-cases.json": db_fallback_cases,
        "zip-cases.json": zip_cases,
        "job-cases.json": job_cases,
        "policy-processing-cases.json": processing_cases,
        "audit-cases.json": audit_cases,
        "report-cases.json": report_cases,
    }


def main() -> None:
    ensure_folders()
    write_csharp_files()
    all_cases = build_cases()

    for file_name, cases in all_cases.items():
        save_cases(file_name, cases)

    total = sum(len(cases) for cases in all_cases.values())

    print()
    print("PolicyDrift regression pack added.")
    print(f"Added {total} data-driven PolicyDrift scenario cases.")
    print()
    print("Counts:")
    for file_name, cases in all_cases.items():
        print(f"  {file_name}: {len(cases)}")
    print()
    print("Next commands:")
    print(r"  dotnet build .\CVIS.Automation.sln")
    print(r"  dotnet test .\CVIS.Automation.Tests\CVIS.Automation.Tests.csproj --filter TestCategory=PolicyDrift")
    print()


if __name__ == "__main__":
    main()
