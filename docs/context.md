# CVIS.Automation Context

CVIS.Automation is an NUnit automation harness.

NUnit is the primary runner. Playwright is optional and should only be used when browser automation is actually required.

## Official base classes

```text
BaseAutomationCvisTest
BaseAutomationCvisApiTest
BaseAutomationCvisDatabaseTest
BaseAutomationCvisPlaywrightBrowserTest
BaseAutomationCvisPlaywrightPageTabTest
```

## Reporting

`cpn-report.html` is authoritative and generated from TRX/NUnit XML.

`cpn-lifecycle-report.html` is diagnostic only.
