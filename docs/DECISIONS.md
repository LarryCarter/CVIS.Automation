
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

