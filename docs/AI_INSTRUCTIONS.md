# AI Instructions for CVIS.Automation

This repository is designed to be AI-friendly.

## Core rules

1. NUnit is the primary test framework.
2. Playwright is optional and only for browser automation.
3. Do not force all tests to inherit Playwright classes.
4. Do not create domain-specific base classes unless explicitly approved.
5. Prefer capability base classes:
   - `BaseAutomationCvisTest`
   - `BaseAutomationCvisApiTest`
   - `BaseAutomationCvisDatabaseTest`
   - `BaseAutomationCvisPlaywrightBrowserTest`
   - `BaseAutomationCvisPlaywrightPageTabTest`
6. Reports must be generated from TRX/NUnit XML, not lifecycle teardown logs.
7. HyperExecute parses `TestResults\NUnitXml`.
8. `cpn-report.html` is authoritative.
9. `cpn-lifecycle-report.html` is diagnostic only.

## When generating a new test

Ask what capability the test needs:

| Need | Base |
|---|---|
| config/logging only | `BaseAutomationCvisTest` |
| API client | `BaseAutomationCvisApiTest` |
| database connection | `BaseAutomationCvisDatabaseTest` |
| browser without automatic page | `BaseAutomationCvisPlaywrightBrowserTest` |
| browser with fresh page/tab | `BaseAutomationCvisPlaywrightPageTabTest` |

## Avoid

```csharp
PolicyDriftBaseTest
UnityBaseTest
LegacySustainmentBaseTest
SomeApiBaseThatInheritsDatabaseBase
```

Use services/helpers instead of inheritance chains.
