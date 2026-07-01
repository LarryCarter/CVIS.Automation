# CVIS.Automation Memory

## Current architecture

NUnit is the spine.

Playwright is optional.

Developers choose one of five base classes based on test capability:

```text
BaseAutomationCvisTest
BaseAutomationCvisApiTest
BaseAutomationCvisDatabaseTest
BaseAutomationCvisPlaywrightBrowserTest
BaseAutomationCvisPlaywrightPageTabTest
```

## Reporting memory

`TestResults\CPN\cpn-report.html` is authoritative.

`TestResults\CPN\cpn-lifecycle-report.html` is diagnostic.

HyperExecute parses `TestResults\NUnitXml`.
