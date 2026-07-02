
<!-- RDEL-DOCOPS-ID: 9C79045F022DA951 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/context/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-01 12:56:05Z -->

## CVIS.Automation — Clean Base Class Naming and README Standard

RDEL package `contollo.cvis.automation.clean-base-class-naming-doc-standard` establishes clean final naming for CVIS automation base classes.

Canonical base class selection:

| Need | Inherit from |
|---|---|
| Normal NUnit functional test, no browser | `BaseAutomationCvisTest` |
| API test | `BaseAutomationCvisApiTest` |
| SQL/database test | `BaseAutomationCvisDatabaseTest` |
| Playwright browser-level setup | `BaseAutomationCvisPlaywrightBrowserTest` |
| Playwright fresh page/tab per test | `BaseAutomationCvisPlaywrightPageTabTest` |

Old names are retained only as temporary obsolete compatibility aliases where delete/rename support is unavailable.

Authoritative reporting comes from real NUnit/TRX execution output and writes `TestResults\CPN\cpn-report.html`. Lifecycle reporting remains diagnostic only at `TestResults\CPN\cpn-lifecycle-report.html`.


<!-- RDEL-DOCOPS-ID: 9807E72E915B2BD5 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/context/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-01 13:09:16Z -->

## CVIS.Automation — RDEL 1.2.6 Playwright PageTab TestContext Fix

The clean base-class naming update requires `BaseAutomationCvisPlaywrightPageTabTest` to use NUnit `TestContext` when logging fresh page creation. The file must import `NUnit.Framework` because `TestContext` is provided by NUnit.

Canonical target file:

```text
CVIS.Playwright.NUnitCompat/Base/BaseAutomationCvisPlaywrightPageTabTest.cs
```

Do not remove the `using NUnit.Framework;` directive from that file unless the `TestContext` reference is also removed or fully qualified.


<!-- RDEL-DOCOPS-ID: 8C8480278EC46425 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/context/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 05:46:59Z -->

<!-- RDEL-DOCOPS-ID: XUNIT-POLICYDRIFT-FULL-MIGRATION-1-2-8 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/context/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 05:13:37Z -->

## CVIS.Automation — RDEL 1.2.8 xUnit PolicyDrift Full Migration

A new xUnit-only project `Automation.ConsoleApp.Tests` is the canonical target for the migrated PolicyDrift tests. It mirrors the requested layout under `Integration/PolicyDrift` and uses xUnit attributes only.

The existing NUnit project remains in place. The new project is isolated and must not include NUnit packages, NUnit usings, NUnit attributes, or NUnit assertions.


<!-- RDEL-DOCOPS-ID: 902E5CA07C38EB4E -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/context/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 05:51:21Z -->

<!-- RDEL-DOCOPS-ID: XUNIT-CONFIG-PACKAGE-REFS-1-3-0 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/context/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 05:55:00Z -->

## CVIS.Automation - xUnit Configuration Package References Fix

RDEL package `contollo.cvis.automation.xunit.configuration-package-references-fix` fixes the `Automation.ConsoleApp.Tests` project after the xUnit PolicyDrift migration by adding explicit `Microsoft.Extensions.Configuration` package references.

The xUnit project uses `IConfigurationRoot`, `ConfigurationBuilder`, `SetBasePath`, `AddJsonFile`, `AddEnvironmentVariables`, and `GetValue<T>()`, so it requires the corresponding configuration packages under central package management.


<!-- RDEL-DOCOPS-ID: 18D7CF88249C3D27 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/context/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 05:55:06Z -->

<!-- RDEL-DOCOPS-ID: NUNIT-ASSERT-MULTIPLE-FIX-1-3-1 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/context/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 05:13:37Z -->

## CVIS.Automation — NUnit Assert.Multiple Ambiguity Fix

RDEL package `contollo.cvis.automation.nunit-assert-multiple-ambiguity-fix` updates the legacy NUnit `CVIS.Automation.Tests/Examples/PolicyDriftValidationTests.cs` file to avoid the NUnit 4 overload ambiguity between `Assert.Multiple(TestDelegate)` and `Assert.Multiple(Action)`.

The fix preserves the same assertions but executes them directly instead of wrapping them in `Assert.Multiple`.


<!-- RDEL-DOCOPS-ID: 09C4D290055E6762 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/context/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 06:04:31Z -->

<!-- RDEL-DOCOPS-ID: XUNIT-POLICYDRIFT-SCENARIO-EXPANSION-1-3-2 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/context/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 05:13:37Z -->

## CVIS.Automation — xUnit PolicyDrift Scenario Expansion

RDEL package `contollo.cvis.automation.xunit-policydrift-scenario-expansion` updates the new `Automation.ConsoleApp.Tests` xUnit project so PolicyDrift matrix tests expose scenario-driven theory cases using `MemberData` object arrays.

The xUnit project should mirror PolicyDrift coverage from the NUnit project, including API, Console, Database, Workflows, Assertions, Matrix, Models, and TestData areas.


<!-- RDEL-DOCOPS-ID: A7299C7671C23F48 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/context/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 06:06:23Z -->

<!-- RDEL-DOCOPS-ID: XUNIT-LOADJSONARRAY-ACCESSIBILITY-FIX-1-3-3 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/context/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 06:12:00Z -->

## CVIS.Automation — RDEL 1.3.3 xUnit PolicyDrift LoadJsonArray Accessibility Fix

`Automation.ConsoleApp.Tests/UnitTestBase.cs` now exposes `LoadJsonArray<T>(string)` as `public static` so static xUnit `MemberData` providers such as `PolicyDriftScenarioData` can load PolicyDrift JSON scenario files without CS0122 accessibility errors.


<!-- RDEL-DOCOPS-ID: 2E917528E536C484 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/context/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 06:10:42Z -->

<!-- RDEL-DOCOPS-ID: XUNIT-POLICYDRIFT-SCENARIO-COUNT-FIX-1-3-4 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/context/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 05:13:37Z -->

## CVIS.Automation — xUnit PolicyDrift Scenario Count Fix

RDEL package `contollo.cvis.automation.xunit-policydrift-scenario-count-fix` fixes the `Automation.ConsoleApp.Tests` xUnit PolicyDrift migration so the scenario matrix reads from the authoritative source test-data folder:

```text
CVIS.Automation.Tests/Projects/PolicyDrift/TestData
```

when the new xUnit project does not contain a complete copied `Integration/PolicyDrift/TestData` set.

This restores xUnit `[Theory]` expansion for PolicyDrift matrix tests and prevents the migrated project from showing a reduced scenario count.


<!-- RDEL-DOCOPS-ID: 412899E72657E041 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/context/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 06:22:32Z -->

<!-- RDEL-DOCOPS-ID: XUNIT-POLICYDRIFT-DISCOVERY-EXPANSION-1-3-5 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/context/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 05:13:37Z -->

## CVIS.Automation — xUnit PolicyDrift Scenario Discovery Expansion

RDEL package `contollo.cvis.automation.xunit-policydrift-discovery-expansion` updates `Automation.ConsoleApp.Tests` so PolicyDrift xUnit matrix tests expose scenario rows as individual test cases.

The prior xUnit migration still produced collapsed matrix theories in Visual Studio Test Explorer. The fix is to avoid passing custom scenario objects directly through `MemberData`; instead, matrix data providers return primitive values and each test reconstructs `PolicyDriftScenarioCase` inside the test body.

Canonical xUnit PolicyDrift matrix pattern:

```csharp
[Theory]
[MemberData(nameof(PolicyDriftScenarioData.CyberArkPlatformCases), MemberType = typeof(PolicyDriftScenarioData))]
public async Task GetPlatformsFailureOrVariation_ShouldFollowExpectedFallbackBehavior(
    string name,
    string scenarioType,
    string expectedBehavior,
    string expectedFinalStatus,
    int expectedMinimumRecordCount)
{
    var scenario = PolicyDriftScenarioData.CreateScenario(
        name,
        scenarioType,
        expectedBehavior,
        expectedFinalStatus,
        expectedMinimumRecordCount);
}
```

`UnitTestBase.LoadJsonArray<T>` should search both `Automation.ConsoleApp.Tests/Integration/PolicyDrift/TestData` and the original `CVIS.Automation.Tests/Projects/PolicyDrift/TestData` path while the migration remains in parallel with the NUnit project.


<!-- RDEL-DOCOPS-ID: 0B3D4A15BBBDBFF6 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/context/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 06:48:31Z -->

<!-- RDEL-DOCOPS-ID: XUNIT-POLICYDRIFT-FULL-DISCOVERY-1-3-6 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/context/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 05:13:37Z -->

## CVIS.Automation — xUnit PolicyDrift Full Scenario Discovery Fix

RDEL package `contollo.cvis.automation.xunit.policydrift.full-scenario-discovery-fix` updates `Automation.ConsoleApp.Tests` so PolicyDrift xUnit matrix tests use primitive `MemberData` rows rather than complex scenario objects or collapsed harness loops.

The intent is to make Visual Studio/xUnit discover and execute each PolicyDrift scenario JSON row as an individual test case, matching the NUnit scenario matrix behavior more closely.


<!-- RDEL-DOCOPS-ID: 3199EEF23813C38D -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/context/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 06:53:36Z -->

<!-- RDEL-DOCOPS-ID: XUNIT-POLICYDRIFT-SOURCE-TESTDATA-LOADER-1-3-7 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/context/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 06:55:00Z -->

## CVIS.Automation — xUnit PolicyDrift Source TestData Loader Fix

RDEL package `contollo.cvis.automation.xunit.policydrift.source-testdata-loader-fix` updates `Automation.ConsoleApp.Tests/UnitTestBase.cs` so PolicyDrift scenario data resolves against the original NUnit project TestData folder first:

```text
CVIS.Automation.Tests/Projects/PolicyDrift/TestData
```

This is required because the migrated xUnit-local data files may be incomplete, causing xUnit discovery to show far fewer PolicyDrift tests than the source NUnit project.


<!-- RDEL-DOCOPS-ID: E2C97A374164AE94 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/context/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 06:57:25Z -->

<!-- RDEL-DOCOPS-ID: XUNIT-POLICYDRIFT-FULL-TESTDATA-COUNT-FIX-1-3-8 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/context/update.md -->

## CVIS.Automation — xUnit PolicyDrift Full TestData Count Fix

RDEL package `contollo.cvis.automation.xunit-policydrift-full-testdata-count-fix` restores full xUnit PolicyDrift scenario coverage by replacing truncated local xUnit TestData files with full scenario copies. The xUnit matrix loader now loads local files under `Automation.ConsoleApp.Tests/Integration/PolicyDrift/TestData`.


<!-- RDEL-DOCOPS-ID: B3AE0565C6905A88 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/context/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 06:59:27Z -->

<!-- RDEL-DOCOPS-ID: XUNIT-POLICYDRIFT-WORKFLOW-DATA-ALIAS-1-3-9 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/context/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 07:05:00Z -->

## CVIS.Automation — xUnit PolicyDrift Workflow Data Alias Fix

RDEL package `contollo.cvis.automation.xunit-policydrift-workflow-data-alias-fix` adds `PolicyDriftScenarioData.PolicyDriftWorkflowCases` as a compatibility alias for `WorkflowCases` so the xUnit workflow test project compiles after the full PolicyDrift test data migration.

