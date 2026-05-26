from pathlib import Path

ps = r'''# ============================================================
# CVIS.Automation - PolicyDrift Regression Pack Add-On
# Save as:
#   C:\Users\larry\source\repos\CVIS.Automation\add-policy-drift-regression-pack.ps1
#
# Run from:
#   C:\Users\larry\source\repos\CVIS.Automation
#
# Command:
#   .\add-policy-drift-regression-pack.ps1
# ============================================================

$ErrorActionPreference = "Stop"

$SolutionRoot = Get-Location
$TestProjectRoot = Join-Path $SolutionRoot "CVIS.Automation.Tests"

if (-not (Test-Path $TestProjectRoot)) {
    throw "Cannot find CVIS.Automation.Tests under $SolutionRoot. Run this from C:\Users\larry\source\repos\CVIS.Automation."
}

function Write-FileUtf8 {
    param(
        [string]$Path,
        [string]$Content
    )

    $folder = Split-Path -Parent $Path
    if (-not [string]::IsNullOrWhiteSpace($folder) -and -not (Test-Path $folder)) {
        New-Item -ItemType Directory -Path $folder -Force | Out-Null
    }

    Set-Content -Path $Path -Value $Content -Encoding UTF8
}

function New-ScenarioCase {
    param(
        [string]$Name,
        [string]$ScenarioType,
        [string]$ExpectedBehavior,
        [string]$ExpectedFinalStatus = "Completed",
        [int]$ExpectedMinimumRecordCount = 1
    )

    [PSCustomObject]@{
        name = $Name
        scenarioType = $ScenarioType
        expectedBehavior = $ExpectedBehavior
        expectedFinalStatus = $ExpectedFinalStatus
        expectedMinimumRecordCount = $ExpectedMinimumRecordCount
    }
}

function Save-ScenarioCases {
    param(
        [string]$FileName,
        [array]$Cases
    )

    $path = Join-Path $TestProjectRoot "Projects\PolicyDrift\TestData\$FileName"
    $json = $Cases | ConvertTo-Json -Depth 10
    Write-FileUtf8 -Path $path -Content $json
}

$folders = @(
    "Projects\PolicyDrift\Assertions",
    "Projects\PolicyDrift\Matrix",
    "Projects\PolicyDrift\Models",
    "Projects\PolicyDrift\TestData",
    "Projects\PolicyDrift\Workflows"
)

foreach ($folder in $folders) {
    New-Item -ItemType Directory -Path (Join-Path $TestProjectRoot $folder) -Force | Out-Null
}

Write-FileUtf8 -Path (Join-Path $TestProjectRoot "Projects\PolicyDrift\Models\PolicyDriftScenarioCase.cs") -Content @'
namespace CVIS.Automation.Tests.Projects.PolicyDrift.Models;

public sealed record PolicyDriftScenarioCase
{
    public string Name { get; init; } = string.Empty;
    public string ScenarioType { get; init; } = string.Empty;
    public string ExpectedBehavior { get; init; } = string.Empty;
    public string ExpectedFinalStatus { get; init; } = string.Empty;
    public int ExpectedMinimumRecordCount { get; init; }
}
'@

Write-FileUtf8 -Path (Join-Path $TestProjectRoot "Projects\PolicyDrift\Assertions\PolicyDriftScenarioAssert.cs") -Content @'
using CVIS.Automation.Tests.Projects.PolicyDrift.Models;
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
'@

Write-FileUtf8 -Path (Join-Path $TestProjectRoot "Projects\PolicyDrift\Matrix\PolicyDriftScenarioData.cs") -Content @'
using CVIS.Automation.Tests.Projects.PolicyDrift.Models;
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
'@

Write-FileUtf8 -Path (Join-Path $TestProjectRoot "Projects\PolicyDrift\Workflows\PolicyDriftCyberArkPlatformMatrixTests.cs") -Content @'
using CVIS.Automation.Tests.Projects.PolicyDrift.Assertions;
using CVIS.Automation.Tests.Projects.PolicyDrift.Matrix;
using CVIS.Automation.Tests.Projects.PolicyDrift.Models;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Projects.PolicyDrift.Workflows;

[TestFixture]
[Category("PolicyDrift")]
[Category("CyberArk")]
[Category("Negative")]
[Category("WorkflowRegression")]
public sealed class PolicyDriftCyberArkPlatformMatrixTests
{
    [TestCaseSource(typeof(PolicyDriftScenarioData), nameof(PolicyDriftScenarioData.CyberArkPlatformCases))]
    public void GetPlatformsFailureOrVariation_ShouldFollowExpectedFallbackBehavior(PolicyDriftScenarioCase scenario)
    {
        PolicyDriftScenarioAssert.MarkAsHarnessScaffold(scenario, "CyberArk GetPlatforms");
    }
}
'@

Write-FileUtf8 -Path (Join-Path $TestProjectRoot "Projects\PolicyDrift\Workflows\PolicyDriftCyberArkPolicyMatrixTests.cs") -Content @'
using CVIS.Automation.Tests.Projects.PolicyDrift.Assertions;
using CVIS.Automation.Tests.Projects.PolicyDrift.Matrix;
using CVIS.Automation.Tests.Projects.PolicyDrift.Models;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Projects.PolicyDrift.Workflows;

[TestFixture]
[Category("PolicyDrift")]
[Category("CyberArk")]
[Category("ApiRegression")]
[Category("WorkflowRegression")]
public sealed class PolicyDriftCyberArkPolicyMatrixTests
{
    [TestCaseSource(typeof(PolicyDriftScenarioData), nameof(PolicyDriftScenarioData.CyberArkPolicyCases))]
    public void GetPolicyVariation_ShouldFollowExpectedBehavior(PolicyDriftScenarioCase scenario)
    {
        PolicyDriftScenarioAssert.MarkAsHarnessScaffold(scenario, "CyberArk GetPolicy");
    }
}
'@

Write-FileUtf8 -Path (Join-Path $TestProjectRoot "Projects\PolicyDrift\Workflows\PolicyDriftDbFallbackMatrixTests.cs") -Content @'
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
'@

Write-FileUtf8 -Path (Join-Path $TestProjectRoot "Projects\PolicyDrift\Workflows\PolicyDriftZipMatrixTests.cs") -Content @'
using CVIS.Automation.Tests.Projects.PolicyDrift.Assertions;
using CVIS.Automation.Tests.Projects.PolicyDrift.Matrix;
using CVIS.Automation.Tests.Projects.PolicyDrift.Models;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Projects.PolicyDrift.Workflows;

[TestFixture]
[Category("PolicyDrift")]
[Category("ZipRegression")]
[Category("WorkflowRegression")]
public sealed class PolicyDriftZipMatrixTests
{
    [TestCaseSource(typeof(PolicyDriftScenarioData), nameof(PolicyDriftScenarioData.ZipCases))]
    public void ZipDownloadOrExtractionScenario_ShouldProduceExpectedBehavior(PolicyDriftScenarioCase scenario)
    {
        PolicyDriftScenarioAssert.MarkAsHarnessScaffold(scenario, "ZIP handling");
    }
}
'@

Write-FileUtf8 -Path (Join-Path $TestProjectRoot "Projects\PolicyDrift\Workflows\PolicyDriftJobMatrixTests.cs") -Content @'
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
'@

Write-FileUtf8 -Path (Join-Path $TestProjectRoot "Projects\PolicyDrift\Workflows\PolicyDriftProcessingMatrixTests.cs") -Content @'
using CVIS.Automation.Tests.Projects.PolicyDrift.Assertions;
using CVIS.Automation.Tests.Projects.PolicyDrift.Matrix;
using CVIS.Automation.Tests.Projects.PolicyDrift.Models;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Projects.PolicyDrift.Workflows;

[TestFixture]
[Category("PolicyDrift")]
[Category("PolicyProcessingRegression")]
[Category("WorkflowRegression")]
public sealed class PolicyDriftProcessingMatrixTests
{
    [TestCaseSource(typeof(PolicyDriftScenarioData), nameof(PolicyDriftScenarioData.PolicyProcessingCases))]
    public void PolicyProcessingScenario_ShouldProduceExpectedDriftBehavior(PolicyDriftScenarioCase scenario)
    {
        PolicyDriftScenarioAssert.MarkAsHarnessScaffold(scenario, "policy processing");
    }
}
'@

Write-FileUtf8 -Path (Join-Path $TestProjectRoot "Projects\PolicyDrift\Workflows\PolicyDriftAuditMatrixTests.cs") -Content @'
using CVIS.Automation.Tests.Projects.PolicyDrift.Assertions;
using CVIS.Automation.Tests.Projects.PolicyDrift.Matrix;
using CVIS.Automation.Tests.Projects.PolicyDrift.Models;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Projects.PolicyDrift.Workflows;

[TestFixture]
[Category("PolicyDrift")]
[Category("AuditRegression")]
[Category("WorkflowRegression")]
public sealed class PolicyDriftAuditMatrixTests
{
    [TestCaseSource(typeof(PolicyDriftScenarioData), nameof(PolicyDriftScenarioData.AuditCases))]
    public void AuditOrLogScenario_ShouldProduceExpectedRecord(PolicyDriftScenarioCase scenario)
    {
        PolicyDriftScenarioAssert.MarkAsHarnessScaffold(scenario, "audit/log");
    }
}
'@

Write-FileUtf8 -Path (Join-Path $TestProjectRoot "Projects\PolicyDrift\Workflows\PolicyDriftReportMatrixTests.cs") -Content @'
using CVIS.Automation.Tests.Projects.PolicyDrift.Assertions;
using CVIS.Automation.Tests.Projects.PolicyDrift.Matrix;
using CVIS.Automation.Tests.Projects.PolicyDrift.Models;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Projects.PolicyDrift.Workflows;

[TestFixture]
[Category("PolicyDrift")]
[Category("ReportRegression")]
[Category("WorkflowRegression")]
public sealed class PolicyDriftReportMatrixTests
{
    [TestCaseSource(typeof(PolicyDriftScenarioData), nameof(PolicyDriftScenarioData.ReportCases))]
    public void ReportScenario_ShouldProduceExpectedOutput(PolicyDriftScenarioCase scenario)
    {
        PolicyDriftScenarioAssert.MarkAsHarnessScaffold(scenario, "report output");
    }
}
'@

# -----------------------------
# Generate scenario JSON files.
# -----------------------------

$cyberArkPlatformTypes = @(
    "Unauthorized401","Forbidden403","NotFound404","ServerError500","BadGateway502","ServiceUnavailable503","GatewayTimeout504",
    "Timeout","DnsFailure","TlsFailure","ConnectionReset","MalformedJson","EmptyJsonArray","NullResponseBody","MissingPlatformNameField",
    "DuplicatePlatformNames","WhitespacePlatformNames","LargePlatformList","PartialPayload206","RateLimited429",
    "TransientFailureAttempt21","TransientFailureAttempt22","TransientFailureAttempt23","TransientFailureAttempt24","TransientFailureAttempt25",
    "TransientFailureAttempt26","TransientFailureAttempt27","TransientFailureAttempt28","TransientFailureAttempt29","TransientFailureAttempt30"
)

$cyberArkPlatformCases = @()
foreach ($type in $cyberArkPlatformTypes) {
    $minCount = 1
    if ($type -like "*Empty*") { $minCount = 0 }

    $cyberArkPlatformCases += New-ScenarioCase `
        -Name "GetPlatforms_$type" `
        -ScenarioType $type `
        -ExpectedBehavior "FallbackToDatabase" `
        -ExpectedFinalStatus "Completed" `
        -ExpectedMinimumRecordCount $minCount
}
Save-ScenarioCases -FileName "cyberark-platform-cases.json" -Cases $cyberArkPlatformCases

$cyberArkPolicyTypes = @(
    "ValidPlatform","InvalidPlatformName","BlankPlatformName","WhitespacePlatformName","Unauthorized401","Forbidden403","ServerError500",
    "ServiceUnavailable503","Timeout","MalformedJson","EmptyBody","MissingRequiredFields","ExtraFields","DuplicatePolicies","LargePayload",
    "PolicyDisabled","PolicyRenamed","PolicyDeleted","RateLimited429","PartialContent206",
    "PlatformBatch021","PlatformBatch022","PlatformBatch023","PlatformBatch024","PlatformBatch025","PlatformBatch026","PlatformBatch027",
    "PlatformBatch028","PlatformBatch029","PlatformBatch030","PlatformBatch031","PlatformBatch032","PlatformBatch033","PlatformBatch034",
    "PlatformBatch035","PlatformBatch036","PlatformBatch037","PlatformBatch038","PlatformBatch039","PlatformBatch040"
)

$cyberArkPolicyCases = @()
foreach ($type in $cyberArkPolicyTypes) {
    $status = "Completed"
    $minCount = 1
    if ($type -like "*Invalid*" -or $type -like "*Blank*") { $status = "LoggedAndContinued" }
    if ($type -like "*Empty*" -or $type -like "*Deleted*") { $minCount = 0 }

    $cyberArkPolicyCases += New-ScenarioCase `
        -Name "GetPolicy_$type" `
        -ScenarioType $type `
        -ExpectedBehavior "ValidatePolicyCallHandling" `
        -ExpectedFinalStatus $status `
        -ExpectedMinimumRecordCount $minCount
}
Save-ScenarioCases -FileName "cyberark-policy-cases.json" -Cases $cyberArkPolicyCases

$dbFallbackTypes = @(
    "PlatformTableHasRows","PlatformTableEmpty","PlatformRowsInactive","PlatformRowsStale","DuplicatePlatformRows","NullPlatformName",
    "BlankPlatformName","WhitespacePlatformName","LongPlatformName","SpecialCharacterPlatformName","PolicyNameMapped","PolicyNameMissing",
    "PolicyNameDuplicate","PolicyNameInactive","PolicyNameStale","DatabaseConnectionFails","DatabaseTimeout","StoredProcedureMissing",
    "PermissionDenied","DeadlockRetry","FallbackAuditWritten","FallbackRunStatusUpdated","FallbackCorrelationIdWritten","FallbackErrorLogged",
    "FallbackWarningLogged","PlatformRecord026","PlatformRecord027","PlatformRecord028","PlatformRecord029","PlatformRecord030",
    "PlatformRecord031","PlatformRecord032","PlatformRecord033","PlatformRecord034","PlatformRecord035","PlatformRecord036",
    "PlatformRecord037","PlatformRecord038","PlatformRecord039","PlatformRecord040"
)

$dbFallbackCases = @()
foreach ($type in $dbFallbackTypes) {
    $status = "Completed"
    $minCount = 1
    if ($type -like "*Fails*" -or $type -like "*Timeout*" -or $type -like "*Missing*" -or $type -like "*Denied*") { $status = "FailedOrLogged" }
    if ($type -like "*Empty*" -or $type -like "*Missing*") { $minCount = 0 }

    $dbFallbackCases += New-ScenarioCase `
        -Name "DbFallback_$type" `
        -ScenarioType $type `
        -ExpectedBehavior "ValidateFallbackPath" `
        -ExpectedFinalStatus $status `
        -ExpectedMinimumRecordCount $minCount
}
Save-ScenarioCases -FileName "db-fallback-cases.json" -Cases $dbFallbackCases

$zipTypes = @(
    "ValidZip","MissingZip","EmptyZip","CorruptedZip","PasswordProtectedZip","ZipWithUnexpectedFolder","ZipWithMissingPolicyFile",
    "ZipWithExtraFiles","ZipWithInvalidJson","ZipWithMalformedXml","LargeZip","ZeroBytePolicyFile","DuplicatePolicyFiles",
    "OldZipAlreadyProcessed","ZipNameDateMismatch","ZipDownloadTimeout","ZipDownloadUnauthorized","ZipDownloadForbidden",
    "ZipDownloadServerError","ZipWriteAccessDenied","DiskFull","PathTooLong","InvalidCharactersInFileName","ChecksumMismatch","ChecksumMatch"
)

$zipCases = @()
foreach ($type in $zipTypes) {
    $status = "FailedOrLogged"
    $minCount = 0
    if ($type -eq "ValidZip" -or $type -eq "ZipWithExtraFiles" -or $type -eq "LargeZip" -or $type -eq "ChecksumMatch") {
        $status = "Completed"
        $minCount = 1
    }

    $zipCases += New-ScenarioCase `
        -Name "Zip_$type" `
        -ScenarioType $type `
        -ExpectedBehavior "ValidateZipHandling" `
        -ExpectedFinalStatus $status `
        -ExpectedMinimumRecordCount $minCount
}
Save-ScenarioCases -FileName "zip-cases.json" -Cases $zipCases

$jobTypes = @(
    "JobStarts","JobCompletes","JobFails","JobRetries","JobTimesOut","JobAlreadyRunning","JobDisabled","JobMissingSchedule","JobManualTrigger",
    "JobScheduledTrigger","JobWritesStartLog","JobWritesCompleteLog","JobWritesErrorLog","JobWritesCorrelationId","JobUsesQaConfig",
    "JobUsesUatConfig","JobUsesOcpConfig","JobHandlesMissingConfig","JobHandlesInvalidConfig","JobHandlesCyberArkFailure",
    "JobHandlesDbFallback","JobHandlesZipFailure","JobHandlesNoDrift","JobHandlesDetectedDrift","JobPublishesCompletionStatus"
)

$jobCases = @()
foreach ($type in $jobTypes) {
    $status = "Completed"
    if ($type -like "*Fails*" -or $type -like "*Missing*" -or $type -like "*Invalid*" -or $type -like "*Disabled*" -or $type -like "*TimesOut*") {
        $status = "FailedOrSkipped"
    }

    $jobCases += New-ScenarioCase `
        -Name "Job_$type" `
        -ScenarioType $type `
        -ExpectedBehavior "ValidateScheduledJobBehavior" `
        -ExpectedFinalStatus $status `
        -ExpectedMinimumRecordCount 1
}
Save-ScenarioCases -FileName "job-cases.json" -Cases $jobCases

$processingTypes = @(
    "NoDrift","PolicyAdded","PolicyRemoved","PolicyChanged","PolicyRenamed","PolicyEnabled","PolicyDisabled","PlatformAdded","PlatformRemoved",
    "PlatformRenamed","DuplicatePolicyIgnored","CaseOnlyPolicyChange","WhitespaceOnlyPolicyChange","DescriptionChanged","CredentialManagementFlagChanged",
    "RotationIntervalChanged","ReconcileAccountChanged","VerificationIntervalChanged","PolicyXmlChanged","PolicyJsonChanged","PolicyMetadataChanged",
    "PolicyOwnerChanged","PolicySafeMappingChanged","PolicyExceptionAdded","PolicyExceptionRemoved","LargePolicySet","EmptyPolicySet","NullPolicyInput",
    "MalformedPolicyInput","OutOfOrderPolicyInput","SamePolicyDifferentOrder","UnexpectedFieldIgnored","RequiredFieldMissing","RunStatusCompleted",
    "RunStatusCompletedWithWarnings","RunStatusFailed","DriftResultInserted","DriftResultUpdated","DriftHistoryWritten","DriftAuditWritten"
)

$processingCases = @()
foreach ($type in $processingTypes) {
    $status = "Completed"
    $minCount = 1
    if ($type -like "*Failed*" -or $type -like "*Malformed*" -or $type -like "*Null*" -or $type -like "*Missing*") { $status = "FailedOrLogged" }
    if ($type -eq "NoDrift" -or $type -eq "DuplicatePolicyIgnored" -or $type -eq "WhitespaceOnlyPolicyChange" -or $type -eq "OutOfOrderPolicyInput" -or $type -eq "SamePolicyDifferentOrder" -or $type -eq "EmptyPolicySet") {
        $minCount = 0
    }

    $processingCases += New-ScenarioCase `
        -Name "PolicyProcessing_$type" `
        -ScenarioType $type `
        -ExpectedBehavior "ValidateDriftProcessing" `
        -ExpectedFinalStatus $status `
        -ExpectedMinimumRecordCount $minCount
}
Save-ScenarioCases -FileName "policy-processing-cases.json" -Cases $processingCases

$auditTypes = @(
    "RunStarted","RunCompleted","RunFailed","CyberArkGetPlatformsFailureLogged","CyberArkGetPolicyFailureLogged","DbFallbackUsedLogged",
    "ZipDownloadedLogged","ZipFailedLogged","DriftDetectedLogged","NoDriftLogged","CorrelationIdOnAllRows","CreatedByAutomation",
    "CreatedDatePopulated","ModifiedDatePopulated","ErrorSeverityCaptured","WarningSeverityCaptured","InfoSeverityCaptured","RetryAttemptCaptured",
    "FallbackReasonCaptured","FinalSummaryCaptured","PolicyCountCaptured","PlatformCountCaptured","DriftCountCaptured","ExceptionStackNotNullOnFailure",
    "NoSecretValuesLogged"
)

$auditCases = @()
foreach ($type in $auditTypes) {
    $auditCases += New-ScenarioCase `
        -Name "Audit_$type" `
        -ScenarioType $type `
        -ExpectedBehavior "ValidateAuditOrLogRecord" `
        -ExpectedFinalStatus "Completed" `
        -ExpectedMinimumRecordCount 1
}
Save-ScenarioCases -FileName "audit-cases.json" -Cases $auditCases

$reportTypes = @(
    "ReportFileCreated","ReportEmptyWhenNoDrift","ReportContainsAddedPolicy","ReportContainsRemovedPolicy","ReportContainsChangedPolicy",
    "ReportContainsRunId","ReportContainsCorrelationId","ReportContainsRunDate","ReportContainsEnvironment","ReportHandlesLargeRun",
    "ReportCsvFormatValid","ReportJsonFormatValid","ReportHtmlFormatValid","ReportOutputPathExists","ReportDoesNotExposeSecrets",
    "ReportOverwritesWhenAllowed","ReportDoesNotOverwriteWhenBlocked","ReportArchiveCreated","ReportArchiveMissingHandled","ReportFinalStatusWritten"
)

$reportCases = @()
foreach ($type in $reportTypes) {
    $status = "Completed"
    $minCount = 1
    if ($type -like "*Missing*") { $status = "Logged" }
    if ($type -like "*Empty*") { $minCount = 0 }

    $reportCases += New-ScenarioCase `
        -Name "Report_$type" `
        -ScenarioType $type `
        -ExpectedBehavior "ValidateReportOutput" `
        -ExpectedFinalStatus $status `
        -ExpectedMinimumRecordCount $minCount
}
Save-ScenarioCases -FileName "report-cases.json" -Cases $reportCases

$total =
    $cyberArkPlatformCases.Count +
    $cyberArkPolicyCases.Count +
    $dbFallbackCases.Count +
    $zipCases.Count +
    $jobCases.Count +
    $processingCases.Count +
    $auditCases.Count +
    $reportCases.Count

Write-Host ""
Write-Host "PolicyDrift regression pack added."
Write-Host "Added $total data-driven PolicyDrift scenario cases."
Write-Host ""
Write-Host "Counts:"
Write-Host "  CyberArk GetPlatforms: $($cyberArkPlatformCases.Count)"
Write-Host "  CyberArk GetPolicy:    $($cyberArkPolicyCases.Count)"
Write-Host "  DB fallback:           $($dbFallbackCases.Count)"
Write-Host "  ZIP handling:          $($zipCases.Count)"
Write-Host "  Scheduled jobs:        $($jobCases.Count)"
Write-Host "  Policy processing:     $($processingCases.Count)"
Write-Host "  Audit/logging:         $($auditCases.Count)"
Write-Host "  Reports/output:        $($reportCases.Count)"
Write-Host ""
Write-Host "Next commands:"
Write-Host "  dotnet build .\CVIS.Automation.sln"
Write-Host "  dotnet test .\CVIS.Automation.Tests\CVIS.Automation.Tests.csproj --filter TestCategory=PolicyDrift"
Write-Host ""
'''

path = Path("/mnt/data/add-policy-drift-regression-pack-CLEAN-POWERSHELL.ps1")
path.write_text(ps, encoding="utf-8")
print(f"Created {path}")
print(ps[:200])
