
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

