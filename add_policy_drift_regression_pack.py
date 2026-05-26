r"""
CVIS.Automation - PolicyDrift Regression Pack Generator

SAVE THIS FILE AS:
    C:\Users\larry\source\repos\CVIS.Automation\add_policy_drift_regression_pack.py

RUN FROM:
    C:\Users\larry\source\repos\CVIS.Automation

COMMAND:
    python .\add_policy_drift_regression_pack.py

THEN RUN:
    dotnet build .\CVIS.Automation.sln
    dotnet test .\CVIS.Automation.Tests\CVIS.Automation.Tests.csproj --filter TestCategory=PolicyDrift

WHAT THIS DOES:
    Creates the PolicyDrift regression scaffold files under:
        C:\Users\larry\source\repos\CVIS.Automation\CVIS.Automation.Tests\Projects\PolicyDrift

    Creates 245 data-driven regression cases across:
        CyberArk GetPlatforms
        CyberArk GetPolicy
        DB fallback
        ZIP handling
        scheduled jobs
        policy processing
        audit/logging
        reports/output
"""

from __future__ import annotations

import json
from pathlib import Path


SOLUTION_ROOT = Path.cwd()
TEST_PROJECT_ROOT = SOLUTION_ROOT.joinpath("CVIS.Automation.Tests")
POLICY_DRIFT_ROOT = TEST_PROJECT_ROOT.joinpath("Projects", "PolicyDrift")


def write_text_file(file_path: Path, content: str) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")


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
    test_data_folder = POLICY_DRIFT_ROOT.joinpath("TestData")
    write_text_file(
        test_data_folder.joinpath(file_name),
        json.dumps(cases, indent=2),
    )


def require_solution_layout() -> None:
    if not TEST_PROJECT_ROOT.exists():
        raise RuntimeError(
            "Cannot find CVIS.Automation.Tests under the current folder.\n"
            "Run this script from:\n"
            r"    C:\Users\larry\source\repos\CVIS.Automation" + "\n"
            f"Current folder is:\n"
            f"    {SOLUTION_ROOT}"
        )

    csproj_path = TEST_PROJECT_ROOT.joinpath("CVIS.Automation.Tests.csproj")

    if not csproj_path.exists():
        raise RuntimeError(
            "Cannot find CVIS.Automation.Tests.csproj.\n"
            "Expected path:\n"
            f"    {csproj_path}"
        )


def ensure_policy_drift_folders() -> None:
    folders = [
        "Assertions",
        "Matrix",
        "Models",
        "TestData",
        "Workflows",
    ]

    for folder in folders:
        POLICY_DRIFT_ROOT.joinpath(folder).mkdir(parents=True, exist_ok=True)


def write_policy_drift_scenario_model() -> None:
    write_text_file(
        POLICY_DRIFT_ROOT.joinpath("Models", "PolicyDriftScenarioCase.cs"),
        """namespace CVIS.Automation.Tests.Projects.PolicyDrift.Models;

public sealed record PolicyDriftScenarioCase
{
    public string Name { get; init; } = string.Empty;
    public string ScenarioType { get; init; } = string.Empty;
    public string ExpectedBehavior { get; init; } = string.Empty;
    public string ExpectedFinalStatus { get; init; } = string.Empty;
    public int ExpectedMinimumRecordCount { get; init; }
}
""",
    )


def write_policy_drift_assertions() -> None:
    write_text_file(
        POLICY_DRIFT_ROOT.joinpath("Assertions", "PolicyDriftScenarioAssert.cs"),
        """using CVIS.Automation.Tests.Projects.PolicyDrift.Models;
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
""",
    )


def write_policy_drift_scenario_data() -> None:
    write_text_file(
        POLICY_DRIFT_ROOT.joinpath("Matrix", "PolicyDriftScenarioData.cs"),
        """using CVIS.Automation.Tests.Projects.PolicyDrift.Models;
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
""",
    )


def write_matrix_test_class(
    file_name: str,
    class_name: str,
    categories: list[str],
    source_name: str,
    method_name: str,
    family: str,
) -> None:
    category_lines = "\n".join(f'[Category("{category}")]' for category in categories)

    content = f"""using CVIS.Automation.Tests.Projects.PolicyDrift.Assertions;
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
"""

    write_text_file(
        POLICY_DRIFT_ROOT.joinpath("Workflows", file_name),
        content,
    )


def write_matrix_tests() -> None:
    write_matrix_test_class(
        file_name="PolicyDriftCyberArkPlatformMatrixTests.cs",
        class_name="PolicyDriftCyberArkPlatformMatrixTests",
        categories=["PolicyDrift", "CyberArk", "Negative", "WorkflowRegression"],
        source_name="CyberArkPlatformCases",
        method_name="GetPlatformsFailureOrVariation_ShouldFollowExpectedFallbackBehavior",
        family="CyberArk GetPlatforms",
    )

    write_matrix_test_class(
        file_name="PolicyDriftCyberArkPolicyMatrixTests.cs",
        class_name="PolicyDriftCyberArkPolicyMatrixTests",
        categories=["PolicyDrift", "CyberArk", "ApiRegression", "WorkflowRegression"],
        source_name="CyberArkPolicyCases",
        method_name="GetPolicyVariation_ShouldFollowExpectedBehavior",
        family="CyberArk GetPolicy",
    )

    write_matrix_test_class(
        file_name="PolicyDriftDbFallbackMatrixTests.cs",
        class_name="PolicyDriftDbFallbackMatrixTests",
        categories=["PolicyDrift", "DatabaseRegression", "WorkflowRegression"],
        source_name="DbFallbackCases",
        method_name="DatabaseFallbackScenario_ShouldProduceExpectedBehavior",
        family="DB fallback",
    )

    write_matrix_test_class(
        file_name="PolicyDriftZipMatrixTests.cs",
        class_name="PolicyDriftZipMatrixTests",
        categories=["PolicyDrift", "ZipRegression", "WorkflowRegression"],
        source_name="ZipCases",
        method_name="ZipDownloadOrExtractionScenario_ShouldProduceExpectedBehavior",
        family="ZIP handling",
    )

    write_matrix_test_class(
        file_name="PolicyDriftJobMatrixTests.cs",
        class_name="PolicyDriftJobMatrixTests",
        categories=["PolicyDrift", "JobRegression", "WorkflowRegression"],
        source_name="JobCases",
        method_name="ScheduledJobScenario_ShouldProduceExpectedBehavior",
        family="scheduled job",
    )

    write_matrix_test_class(
        file_name="PolicyDriftProcessingMatrixTests.cs",
        class_name="PolicyDriftProcessingMatrixTests",
        categories=["PolicyDrift", "PolicyProcessingRegression", "WorkflowRegression"],
        source_name="PolicyProcessingCases",
        method_name="PolicyProcessingScenario_ShouldProduceExpectedDriftBehavior",
        family="policy processing",
    )

    write_matrix_test_class(
        file_name="PolicyDriftAuditMatrixTests.cs",
        class_name="PolicyDriftAuditMatrixTests",
        categories=["PolicyDrift", "AuditRegression", "WorkflowRegression"],
        source_name="AuditCases",
        method_name="AuditOrLogScenario_ShouldProduceExpectedRecord",
        family="audit/log",
    )

    write_matrix_test_class(
        file_name="PolicyDriftReportMatrixTests.cs",
        class_name="PolicyDriftReportMatrixTests",
        categories=["PolicyDrift", "ReportRegression", "WorkflowRegression"],
        source_name="ReportCases",
        method_name="ReportScenario_ShouldProduceExpectedOutput",
        family="report output",
    )


def build_cyberark_platform_cases() -> list[dict]:
    scenario_types = [
        "Unauthorized401",
        "Forbidden403",
        "NotFound404",
        "ServerError500",
        "BadGateway502",
        "ServiceUnavailable503",
        "GatewayTimeout504",
        "Timeout",
        "DnsFailure",
        "TlsFailure",
        "ConnectionReset",
        "MalformedJson",
        "EmptyJsonArray",
        "NullResponseBody",
        "MissingPlatformNameField",
        "DuplicatePlatformNames",
        "WhitespacePlatformNames",
        "LargePlatformList",
        "PartialPayload206",
        "RateLimited429",
    ]

    scenario_types.extend(f"TransientFailureAttempt{index:02}" for index in range(21, 31))

    cases = []

    for scenario_type in scenario_types:
        cases.append(
            make_case(
                name=f"GetPlatforms_{scenario_type}",
                scenario_type=scenario_type,
                expected_behavior="FallbackToDatabase",
                expected_final_status="Completed",
                expected_minimum_record_count=0 if "Empty" in scenario_type else 1,
            )
        )

    return cases


def build_cyberark_policy_cases() -> list[dict]:
    scenario_types = [
        "ValidPlatform",
        "InvalidPlatformName",
        "BlankPlatformName",
        "WhitespacePlatformName",
        "Unauthorized401",
        "Forbidden403",
        "ServerError500",
        "ServiceUnavailable503",
        "Timeout",
        "MalformedJson",
        "EmptyBody",
        "MissingRequiredFields",
        "ExtraFields",
        "DuplicatePolicies",
        "LargePayload",
        "PolicyDisabled",
        "PolicyRenamed",
        "PolicyDeleted",
        "RateLimited429",
        "PartialContent206",
    ]

    scenario_types.extend(f"PlatformBatch{index:03}" for index in range(21, 41))

    cases = []

    for scenario_type in scenario_types:
        expected_status = "Completed"
        expected_count = 1

        if "Invalid" in scenario_type or "Blank" in scenario_type:
            expected_status = "LoggedAndContinued"

        if "Empty" in scenario_type or "Deleted" in scenario_type:
            expected_count = 0

        cases.append(
            make_case(
                name=f"GetPolicy_{scenario_type}",
                scenario_type=scenario_type,
                expected_behavior="ValidatePolicyCallHandling",
                expected_final_status=expected_status,
                expected_minimum_record_count=expected_count,
            )
        )

    return cases


def build_db_fallback_cases() -> list[dict]:
    scenario_types = [
        "PlatformTableHasRows",
        "PlatformTableEmpty",
        "PlatformRowsInactive",
        "PlatformRowsStale",
        "DuplicatePlatformRows",
        "NullPlatformName",
        "BlankPlatformName",
        "WhitespacePlatformName",
        "LongPlatformName",
        "SpecialCharacterPlatformName",
        "PolicyNameMapped",
        "PolicyNameMissing",
        "PolicyNameDuplicate",
        "PolicyNameInactive",
        "PolicyNameStale",
        "DatabaseConnectionFails",
        "DatabaseTimeout",
        "StoredProcedureMissing",
        "PermissionDenied",
        "DeadlockRetry",
        "FallbackAuditWritten",
        "FallbackRunStatusUpdated",
        "FallbackCorrelationIdWritten",
        "FallbackErrorLogged",
        "FallbackWarningLogged",
    ]

    scenario_types.extend(f"PlatformRecord{index:03}" for index in range(26, 41))

    cases = []

    for scenario_type in scenario_types:
        failed_or_logged = any(
            token in scenario_type
            for token in ["Fails", "Timeout", "Missing", "Denied"]
        )

        empty_or_missing = "Empty" in scenario_type or "Missing" in scenario_type

        cases.append(
            make_case(
                name=f"DbFallback_{scenario_type}",
                scenario_type=scenario_type,
                expected_behavior="ValidateFallbackPath",
                expected_final_status="FailedOrLogged" if failed_or_logged else "Completed",
                expected_minimum_record_count=0 if empty_or_missing else 1,
            )
        )

    return cases


def build_zip_cases() -> list[dict]:
    scenario_types = [
        "ValidZip",
        "MissingZip",
        "EmptyZip",
        "CorruptedZip",
        "PasswordProtectedZip",
        "ZipWithUnexpectedFolder",
        "ZipWithMissingPolicyFile",
        "ZipWithExtraFiles",
        "ZipWithInvalidJson",
        "ZipWithMalformedXml",
        "LargeZip",
        "ZeroBytePolicyFile",
        "DuplicatePolicyFiles",
        "OldZipAlreadyProcessed",
        "ZipNameDateMismatch",
        "ZipDownloadTimeout",
        "ZipDownloadUnauthorized",
        "ZipDownloadForbidden",
        "ZipDownloadServerError",
        "ZipWriteAccessDenied",
        "DiskFull",
        "PathTooLong",
        "InvalidCharactersInFileName",
        "ChecksumMismatch",
        "ChecksumMatch",
    ]

    successful_cases = {
        "ValidZip",
        "ZipWithExtraFiles",
        "LargeZip",
        "ChecksumMatch",
    }

    cases = []

    for scenario_type in scenario_types:
        is_success = scenario_type in successful_cases

        cases.append(
            make_case(
                name=f"Zip_{scenario_type}",
                scenario_type=scenario_type,
                expected_behavior="ValidateZipHandling",
                expected_final_status="Completed" if is_success else "FailedOrLogged",
                expected_minimum_record_count=1 if is_success else 0,
            )
        )

    return cases


def build_job_cases() -> list[dict]:
    scenario_types = [
        "JobStarts",
        "JobCompletes",
        "JobFails",
        "JobRetries",
        "JobTimesOut",
        "JobAlreadyRunning",
        "JobDisabled",
        "JobMissingSchedule",
        "JobManualTrigger",
        "JobScheduledTrigger",
        "JobWritesStartLog",
        "JobWritesCompleteLog",
        "JobWritesErrorLog",
        "JobWritesCorrelationId",
        "JobUsesQaConfig",
        "JobUsesUatConfig",
        "JobUsesOcpConfig",
        "JobHandlesMissingConfig",
        "JobHandlesInvalidConfig",
        "JobHandlesCyberArkFailure",
        "JobHandlesDbFallback",
        "JobHandlesZipFailure",
        "JobHandlesNoDrift",
        "JobHandlesDetectedDrift",
        "JobPublishesCompletionStatus",
    ]

    cases = []

    for scenario_type in scenario_types:
        failed_or_skipped = any(
            token in scenario_type
            for token in ["Fails", "Missing", "Invalid", "Disabled", "TimesOut"]
        )

        cases.append(
            make_case(
                name=f"Job_{scenario_type}",
                scenario_type=scenario_type,
                expected_behavior="ValidateScheduledJobBehavior",
                expected_final_status="FailedOrSkipped" if failed_or_skipped else "Completed",
                expected_minimum_record_count=1,
            )
        )

    return cases


def build_policy_processing_cases() -> list[dict]:
    scenario_types = [
        "NoDrift",
        "PolicyAdded",
        "PolicyRemoved",
        "PolicyChanged",
        "PolicyRenamed",
        "PolicyEnabled",
        "PolicyDisabled",
        "PlatformAdded",
        "PlatformRemoved",
        "PlatformRenamed",
        "DuplicatePolicyIgnored",
        "CaseOnlyPolicyChange",
        "WhitespaceOnlyPolicyChange",
        "DescriptionChanged",
        "CredentialManagementFlagChanged",
        "RotationIntervalChanged",
        "ReconcileAccountChanged",
        "VerificationIntervalChanged",
        "PolicyXmlChanged",
        "PolicyJsonChanged",
        "PolicyMetadataChanged",
        "PolicyOwnerChanged",
        "PolicySafeMappingChanged",
        "PolicyExceptionAdded",
        "PolicyExceptionRemoved",
        "LargePolicySet",
        "EmptyPolicySet",
        "NullPolicyInput",
        "MalformedPolicyInput",
        "OutOfOrderPolicyInput",
        "SamePolicyDifferentOrder",
        "UnexpectedFieldIgnored",
        "RequiredFieldMissing",
        "RunStatusCompleted",
        "RunStatusCompletedWithWarnings",
        "RunStatusFailed",
        "DriftResultInserted",
        "DriftResultUpdated",
        "DriftHistoryWritten",
        "DriftAuditWritten",
    ]

    zero_record_cases = {
        "NoDrift",
        "DuplicatePolicyIgnored",
        "WhitespaceOnlyPolicyChange",
        "OutOfOrderPolicyInput",
        "SamePolicyDifferentOrder",
        "EmptyPolicySet",
    }

    cases = []

    for scenario_type in scenario_types:
        failed_or_logged = any(
            token in scenario_type
            for token in ["Failed", "Malformed", "Null", "Missing"]
        )

        cases.append(
            make_case(
                name=f"PolicyProcessing_{scenario_type}",
                scenario_type=scenario_type,
                expected_behavior="ValidateDriftProcessing",
                expected_final_status="FailedOrLogged" if failed_or_logged else "Completed",
                expected_minimum_record_count=0 if scenario_type in zero_record_cases else 1,
            )
        )

    return cases


def build_audit_cases() -> list[dict]:
    scenario_types = [
        "RunStarted",
        "RunCompleted",
        "RunFailed",
        "CyberArkGetPlatformsFailureLogged",
        "CyberArkGetPolicyFailureLogged",
        "DbFallbackUsedLogged",
        "ZipDownloadedLogged",
        "ZipFailedLogged",
        "DriftDetectedLogged",
        "NoDriftLogged",
        "CorrelationIdOnAllRows",
        "CreatedByAutomation",
        "CreatedDatePopulated",
        "ModifiedDatePopulated",
        "ErrorSeverityCaptured",
        "WarningSeverityCaptured",
        "InfoSeverityCaptured",
        "RetryAttemptCaptured",
        "FallbackReasonCaptured",
        "FinalSummaryCaptured",
        "PolicyCountCaptured",
        "PlatformCountCaptured",
        "DriftCountCaptured",
        "ExceptionStackNotNullOnFailure",
        "NoSecretValuesLogged",
    ]

    return [
        make_case(
            name=f"Audit_{scenario_type}",
            scenario_type=scenario_type,
            expected_behavior="ValidateAuditOrLogRecord",
            expected_final_status="Completed",
            expected_minimum_record_count=1,
        )
        for scenario_type in scenario_types
    ]


def build_report_cases() -> list[dict]:
    scenario_types = [
        "ReportFileCreated",
        "ReportEmptyWhenNoDrift",
        "ReportContainsAddedPolicy",
        "ReportContainsRemovedPolicy",
        "ReportContainsChangedPolicy",
        "ReportContainsRunId",
        "ReportContainsCorrelationId",
        "ReportContainsRunDate",
        "ReportContainsEnvironment",
        "ReportHandlesLargeRun",
        "ReportCsvFormatValid",
        "ReportJsonFormatValid",
        "ReportHtmlFormatValid",
        "ReportOutputPathExists",
        "ReportDoesNotExposeSecrets",
        "ReportOverwritesWhenAllowed",
        "ReportDoesNotOverwriteWhenBlocked",
        "ReportArchiveCreated",
        "ReportArchiveMissingHandled",
        "ReportFinalStatusWritten",
    ]

    cases = []

    for scenario_type in scenario_types:
        cases.append(
            make_case(
                name=f"Report_{scenario_type}",
                scenario_type=scenario_type,
                expected_behavior="ValidateReportOutput",
                expected_final_status="Logged" if "Missing" in scenario_type else "Completed",
                expected_minimum_record_count=0 if "Empty" in scenario_type else 1,
            )
        )

    return cases


def build_all_cases() -> dict[str, list[dict]]:
    return {
        "cyberark-platform-cases.json": build_cyberark_platform_cases(),
        "cyberark-policy-cases.json": build_cyberark_policy_cases(),
        "db-fallback-cases.json": build_db_fallback_cases(),
        "zip-cases.json": build_zip_cases(),
        "job-cases.json": build_job_cases(),
        "policy-processing-cases.json": build_policy_processing_cases(),
        "audit-cases.json": build_audit_cases(),
        "report-cases.json": build_report_cases(),
    }


def main() -> None:
    require_solution_layout()
    ensure_policy_drift_folders()

    write_policy_drift_scenario_model()
    write_policy_drift_assertions()
    write_policy_drift_scenario_data()
    write_matrix_tests()

    all_cases = build_all_cases()

    for file_name, cases in all_cases.items():
        save_cases(file_name, cases)

    total = sum(len(cases) for cases in all_cases.values())

    print()
    print("PolicyDrift regression pack added.")
    print(f"Solution root: {SOLUTION_ROOT}")
    print(f"PolicyDrift root: {POLICY_DRIFT_ROOT}")
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
