
<!-- RDEL-DOCOPS-ID: F1839DE800530144 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/memory/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-01 12:56:05Z -->

## Memory — CVIS Base Class Naming Standard

CVIS.Automation now prefers capability-based base classes over domain-specific base classes. New tests should not create `PolicyDriftBaseTest`, `UnityBaseTest`, or `LegacySustainmentBaseTest`.

Use:

- `BaseAutomationCvisTest` for normal no-browser NUnit tests.
- `BaseAutomationCvisApiTest` for API tests.
- `BaseAutomationCvisDatabaseTest` for SQL/database tests.
- `BaseAutomationCvisPlaywrightBrowserTest` for browser-level Playwright tests.
- `BaseAutomationCvisPlaywrightPageTabTest` for Playwright tests needing a fresh page/tab per test.

Every major folder should have a README.md following the repository README standard: Purpose, Responsibilities, When to use, When NOT to use, Architecture, Examples, Common mistakes, Related folders.


<!-- RDEL-DOCOPS-ID: 12E450E91261BD20 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/memory/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-01 13:09:16Z -->

## RDEL 1.2.6 Memory — Playwright PageTab TestContext Fix

A compile error was found after the clean base-class naming package:

```text
CS0103: The name 'TestContext' does not exist in the current context
```

Cause: `BaseAutomationCvisPlaywrightPageTabTest.cs` referenced `TestContext.CurrentContext.Test.FullName` without importing `NUnit.Framework`.

Fix: add `using NUnit.Framework;` to `CVIS.Playwright.NUnitCompat/Base/BaseAutomationCvisPlaywrightPageTabTest.cs`.


<!-- RDEL-DOCOPS-ID: D15E66C88AC2548A -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/memory/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 05:46:59Z -->

<!-- RDEL-DOCOPS-ID: XUNIT-POLICYDRIFT-FULL-MIGRATION-MEMORY-1-2-8 -->

- RDEL 1.2.8 created/updated `Automation.ConsoleApp.Tests` as the xUnit-only migration target for PolicyDrift tests.
- PolicyDrift NUnit patterns were converted to xUnit `[Fact]`, `[Theory]`, `[InlineData]`, `[MemberData]`, and `[Trait]` patterns.


<!-- RDEL-DOCOPS-ID: CA16E90CB91D7F05 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/memory/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 05:51:21Z -->

<!-- RDEL-DOCOPS-ID: XUNIT-CONFIG-PACKAGE-REFS-MEMORY-1-3-0 -->

- `Automation.ConsoleApp.Tests` requires explicit `Microsoft.Extensions.Configuration` package references because its base/config tests use configuration builder APIs and central package management is enabled.


<!-- RDEL-DOCOPS-ID: C749A7903EE53331 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/memory/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 05:55:06Z -->

<!-- RDEL-DOCOPS-ID: NUNIT-ASSERT-MULTIPLE-FIX-1-3-1 -->

- Fixed legacy NUnit compile ambiguity in `CVIS.Automation.Tests/Examples/PolicyDriftValidationTests.cs` by removing the ambiguous `Assert.Multiple(() => ...)` wrapper while preserving equivalent assertions.


<!-- RDEL-DOCOPS-ID: 952DFDCE14FF1966 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/memory/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 06:04:31Z -->

<!-- RDEL-DOCOPS-ID: XUNIT-POLICYDRIFT-SCENARIO-EXPANSION-1-3-2 -->

- `Automation.ConsoleApp.Tests` is the xUnit-only PolicyDrift migration target.
- Scenario matrix tests must use `[Theory]` with `[MemberData]` returning `IEnumerable<object[]>` to preserve one test case per JSON scenario.
- Runtime-disabled smoke tests should return early instead of using NUnit `Assert.Ignore`.


<!-- RDEL-DOCOPS-ID: D80F9B912FBF1391 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/memory/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 06:06:23Z -->

<!-- RDEL-DOCOPS-ID: XUNIT-LOADJSONARRAY-ACCESSIBILITY-FIX-MEMORY-1-3-3 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/memory/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 06:12:00Z -->

- xUnit static `MemberData` provider classes cannot call protected helpers on `UnitTestBase` unless they inherit from it. Shared JSON scenario loaders used by static providers should be `public static` or live directly in the provider class.


<!-- RDEL-DOCOPS-ID: 3BC7B006F853EBA8 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/memory/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 06:10:42Z -->

<!-- RDEL-DOCOPS-ID: XUNIT-POLICYDRIFT-SCENARIO-COUNT-FIX-1-3-4 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/memory/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 05:13:37Z -->

- The xUnit PolicyDrift migration must preserve scenario count by loading JSON rows from the original `CVIS.Automation.Tests/Projects/PolicyDrift/TestData` directory when the new project has incomplete copied TestData.
- xUnit scenario matrix tests should use `[Theory]` + `[MemberData]`, not a single `[Fact]` per matrix file.


<!-- RDEL-DOCOPS-ID: 8957349D330CA60F -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/memory/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 06:22:32Z -->

<!-- RDEL-DOCOPS-ID: XUNIT-POLICYDRIFT-DISCOVERY-EXPANSION-1-3-5 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/memory/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 05:13:37Z -->

- Automation.ConsoleApp.Tests PolicyDrift matrix tests must preserve the scenario count from CVIS.Automation.Tests.
- xUnit MemberData should use primitive row values rather than custom scenario objects when Visual Studio Test Explorer needs to show each JSON scenario as a separate discovered test.
- PolicyDrift xUnit tests may load scenario data from the original NUnit project test data folder until all data is fully duplicated into the xUnit project.


<!-- RDEL-DOCOPS-ID: 70AD28B560BE79C8 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/memory/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 06:48:31Z -->

<!-- RDEL-DOCOPS-ID: XUNIT-POLICYDRIFT-FULL-DISCOVERY-1-3-6 -->

- `Automation.ConsoleApp.Tests` PolicyDrift matrix tests should expose each scenario as a separate xUnit theory row.
- Avoid complex object-only `MemberData` rows for these migrated PolicyDrift tests because Visual Studio/xUnit may collapse discovery into one test per theory.
- Prefer primitive `MemberData` rows for discoverability: name, scenario type, expected behavior, expected final status, expected count.


<!-- RDEL-DOCOPS-ID: BCDBE88FCEF59181 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/memory/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 06:53:36Z -->

<!-- RDEL-DOCOPS-ID: XUNIT-POLICYDRIFT-SOURCE-TESTDATA-MEMORY-1-3-7 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/memory/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 06:55:00Z -->

## Memory: xUnit PolicyDrift Scenario Count

The xUnit `Automation.ConsoleApp.Tests` PolicyDrift migration must preserve the full source scenario count. When migrated xUnit tests request `Integration/PolicyDrift/TestData/*.json`, the loader should prefer the authoritative original path under `CVIS.Automation.Tests/Projects/PolicyDrift/TestData`.


<!-- RDEL-DOCOPS-ID: B8CBDB0BBFF34EAD -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/memory/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 06:57:25Z -->

<!-- RDEL-DOCOPS-ID: XUNIT-POLICYDRIFT-FULL-TESTDATA-MEMORY-1-3-8 -->

- Automation.ConsoleApp.Tests PolicyDrift xUnit scenario count depends on full local TestData JSON files, not truncated smoke samples.


<!-- RDEL-DOCOPS-ID: 77DF97EA151F69E5 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/memory/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 06:59:27Z -->

<!-- RDEL-DOCOPS-ID: XUNIT-POLICYDRIFT-WORKFLOW-DATA-ALIAS-MEMORY-1-3-9 -->

- Added `PolicyDriftScenarioData.PolicyDriftWorkflowCases` alias for xUnit PolicyDrift workflow tests.


<!-- RDEL-DOCOPS-ID: E2C1B970CC321697 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/memory/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 07:01:59Z -->

<!-- RDEL-DOCOPS-ID: XUNIT-PD-COMPILE-FIX-1-4-0 -->

Remember: Automation.ConsoleApp.Tests matrix data providers require the PolicyDrift model namespace and UnitTestBase must expose Analysis for smoke harness assertions.

## xUnit trait counting compatibility

The external counting tool does not correctly count multiple xUnit `[Trait]` attributes on one method. Use duplicated physical test methods with one trait each when a test must count under multiple categories.
