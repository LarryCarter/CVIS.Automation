# CPN Lifecycle Reporting

This folder contains the CPN lifecycle report system.

## Purpose

The lifecycle report is diagnostic. It helps understand which tests passed through CPN setup/teardown.

## Output

```text
TestResults\CPN\cpn-lifecycle-report.html
TestResults\CPN\cpn-lifecycle-report.json
```

## Not authoritative

Do not use lifecycle reports for HyperExecute totals.

The authoritative report is generated after `dotnet test` by `CVIS.Playwright.Reporting.Tool` from TRX and NUnit XML.
