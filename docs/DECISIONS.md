
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

