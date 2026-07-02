
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

