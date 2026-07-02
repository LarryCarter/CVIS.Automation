
<!-- RDEL-DOCOPS-ID: 8E1260091CBBD42D -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/decisions/ADR-0003-clean-base-class-naming-and-readme-standard.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-01 12:56:05Z -->

## ADR-0003 — Clean Base Class Naming and Repository README Standard

Decision: CVIS.Automation uses capability-based base class names and a consistent README.md standard for major folders.

Accepted names:

```text
BaseAutomationCvisTest
BaseAutomationCvisApiTest
BaseAutomationCvisDatabaseTest
BaseAutomationCvisPlaywrightBrowserTest
BaseAutomationCvisPlaywrightPageTabTest
```

Rejected as new-code names:

```text
BaseFunctionalTest
CVISPlaywrightTest
CVISPageTest
PolicyDriftBaseTest
UnityBaseTest
LegacySustainmentBaseTest
```

Reason: domains are not lifecycle capabilities. Tests should inherit based on capability: normal functional, API, database, browser, or page/tab.

Decision: every major folder README.md should use these sections:

```text
Purpose
Responsibilities
When to use
When NOT to use
Architecture
Examples
Common mistakes
Related folders
```

Decision: `cpn-report.html` is authoritative because it is generated from real NUnit/TRX execution output. `cpn-lifecycle-report.html` is diagnostic only and must not be used as the full test total.


<!-- RDEL-DOCOPS-ID: 7316E2FF9AC6962A -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/decisions/ADR-0004-playwright-page-tab-testcontext-fix.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-01 13:09:16Z -->

## ADR-0004 — Keep NUnit.Framework Import in Playwright PageTab Base

Decision: `BaseAutomationCvisPlaywrightPageTabTest.cs` must import `NUnit.Framework` while it logs via `TestContext.CurrentContext`.

Reason: `TestContext` is an NUnit type. Without the using directive or a fully qualified reference, the Playwright compatibility project fails compilation with CS0103.

Status: Accepted.


<!-- RDEL-DOCOPS-ID: D96F6BB590E48969 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/decisions/ADR-0008-xunit-policydrift-full-migration.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 05:46:59Z -->

<!-- RDEL-DOCOPS-ID: ADR-0008-XUNIT-POLICYDRIFT-FULL-MIGRATION -->

# ADR-0008 — xUnit-only PolicyDrift Migration Project

## Decision

Create/maintain `Automation.ConsoleApp.Tests` as an xUnit-only project for the PolicyDrift migration instead of mixing xUnit into the existing NUnit project.

## Rationale

This preserves the original NUnit project and provides a clean migration surface with isolated package references and xUnit test discovery.

## Consequences

The solution now contains `Automation.ConsoleApp.Tests`. Future PolicyDrift xUnit additions should use this project and the `Integration/PolicyDrift` layout.


<!-- RDEL-DOCOPS-ID: 690C5CAD742101F3 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/decisions/ADR-0009-xunit-configuration-package-references.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 05:51:21Z -->

# ADR-0009 - Add explicit configuration packages for Automation.ConsoleApp.Tests

## Decision

Add explicit Microsoft.Extensions.Configuration package references and central package versions for the new xUnit test project.

## Reason

The xUnit migration introduced tests and helpers using `IConfigurationRoot`, `ConfigurationBuilder`, JSON config loading, environment variables, and binder helpers. These APIs are not supplied by xUnit or Microsoft.NET.Test.Sdk.

## Consequence

The project can compile its configuration-based tests without relying on transitive package assumptions.


<!-- RDEL-DOCOPS-ID: 33C82E0433367FCE -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/decisions/ADR-0009-nunit-assert-multiple-fix.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 05:55:06Z -->

<!-- RDEL-DOCOPS-ID: ADR-0009-NUNIT-ASSERT-MULTIPLE-FIX -->

# ADR-0009 — Avoid Ambiguous NUnit Assert.Multiple Overload

## Decision

For the legacy NUnit `PolicyDriftValidationTests` example test, use direct `Assert.That` statements instead of `Assert.Multiple(() => ...)`.

## Reason

The current package set exposes both `Assert.Multiple(TestDelegate)` and `Assert.Multiple(Action)`, which causes CS0121 overload ambiguity for lambda expressions.

## Consequence

The test compiles without changing the intended validation behavior.


<!-- RDEL-DOCOPS-ID: 14AEE5E2600FD0B1 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/decisions/ADR-0009-xunit-policydrift-scenario-expansion.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 06:04:31Z -->

# ADR-0009 - xUnit PolicyDrift Scenario Expansion

Decision: PolicyDrift scenario matrix tests in `Automation.ConsoleApp.Tests` use xUnit `[Theory]` plus `[MemberData]` object arrays, not NUnit `TestCaseData`.

Reason: xUnit requires `object[]` data rows for `MemberData`; preserving a row per JSON scenario maintains equivalent scenario coverage after migration from NUnit.


<!-- RDEL-DOCOPS-ID: 21C73D8043D00E41 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/decisions/ADR-0010-xunit-loadjsonarray-accessibility-fix.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 06:06:23Z -->

<!-- RDEL-DOCOPS-ID: ADR-0010-XUNIT-LOADJSONARRAY-ACCESSIBILITY-FIX -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/decisions/ADR-0010-xunit-loadjsonarray-accessibility-fix.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 06:12:00Z -->

## ADR-0010 — Expose shared xUnit JSON test-data loader

Decision: make `UnitTestBase.LoadJsonArray<T>(string)` public static.

Reason: `PolicyDriftScenarioData` is a static xUnit data provider and must access the loader without inheriting from `UnitTestBase`.


<!-- RDEL-DOCOPS-ID: 7F3C7E022F2950F0 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/decisions/ADR-0009-xunit-policydrift-scenario-count-fix.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 06:10:42Z -->

<!-- RDEL-DOCOPS-ID: XUNIT-POLICYDRIFT-SCENARIO-COUNT-FIX-1-3-4 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/decisions/ADR-0009-xunit-policydrift-scenario-count-fix.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 05:13:37Z -->

# ADR-0009 — xUnit PolicyDrift Scenario Data Source

## Decision

The xUnit `Automation.ConsoleApp.Tests` PolicyDrift scenario matrix will resolve JSON scenario data from the new project first, then fall back to the authoritative NUnit project path:

```text
CVIS.Automation.Tests/Projects/PolicyDrift/TestData
```

## Reason

The initial migration copied only a subset of scenario data, causing the xUnit test count to be much lower than the source NUnit test count.

## Consequence

xUnit theory discovery can expand the same scenario rows as the source PolicyDrift test suite without requiring every JSON file to be physically duplicated into the new project.


<!-- RDEL-DOCOPS-ID: 5B0C310D310D275C -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/decisions/ADR-0009-xunit-policydrift-discovery-expansion.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 06:22:32Z -->

<!-- RDEL-DOCOPS-ID: ADR-0009-XUNIT-POLICYDRIFT-DISCOVERY-EXPANSION -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/decisions/ADR-0009-xunit-policydrift-discovery-expansion.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 05:13:37Z -->

# ADR-0009 — xUnit PolicyDrift Scenario Discovery Expansion

## Status

Accepted

## Context

The initial xUnit migration compiled and passed but discovered far fewer PolicyDrift tests than the NUnit project. Visual Studio Test Explorer showed one xUnit theory per matrix class instead of the full scenario matrix.

## Decision

Use primitive `MemberData` row values for xUnit matrix tests and reconstruct scenario records inside the test body.

## Consequences

- Scenario count becomes visible and comparable to the original NUnit matrix.
- The xUnit project avoids NUnit-only `TestCaseData`.
- Test data loading remains compatible with both new and original PolicyDrift test data locations.


<!-- RDEL-DOCOPS-ID: DCEE33A73D2FF0DF -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/decisions/ADR-0009-xunit-policydrift-full-discovery.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-02 06:48:31Z -->

# ADR-0009 - xUnit PolicyDrift Full Scenario Discovery

## Decision

PolicyDrift xUnit scenario matrices should use primitive `MemberData` rows instead of complex scenario objects.

## Reason

The NUnit source project reports hundreds of individual PolicyDrift scenario tests. The xUnit migration was still reporting far fewer tests because matrix scenarios were being collapsed under each theory/harness method.

## Consequence

Each scenario JSON row is represented as its own xUnit theory row, improving Visual Studio Test Explorer parity with the NUnit project.

