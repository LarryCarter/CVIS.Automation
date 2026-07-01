
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

