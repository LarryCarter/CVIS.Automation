# Authoritative Test Reporting

## Problem

The old CPN HTML report was generated from CPN teardown.

That means it only saw tests inheriting from:

```csharp
CVISPlaywrightTest
CVISBrowserTest
CVISContextTest
CVISPageTest
CVISApiTest
```

That is why it could show only 2 tests while Visual Studio showed hundreds or thousands.

## Correct source of truth

The correct source of truth is the actual test runner output:

```text
TestResults\TRX
TestResults\NUnitXml
```

The authoritative CPN HTML is generated after `dotnet test` from those result files.

## Projects added

```text
CVIS.Playwright.Reporting
CVIS.Playwright.Reporting.Tool
```

## Local run

```powershell
.\scripts\run-authoritative-test-report-local.ps1
```

Then open:

```text
TestResults\CPN\cpn-report.html
```

That report should match the actual NUnit/TRX output.

## Lifecycle report

The lifecycle report is now intentionally separate:

```text
TestResults\CPN\cpn-lifecycle-report.html
```

It is not the report to submit to HyperExecute.

## HyperExecute

Use:

```text
hyperexecute-authoritative-nunit-reporting.yaml
```

HyperExecute parses:

```text
TestResults\NUnitXml
```

with:

```yaml
report: true
partialReports:
  type: nunit
  location: .\TestResults\NUnitXml
  frameworkName: nunit
```

The CPN HTML is uploaded as an artifact:

```text
TestResults\CPN\cpn-report.html
```

## Guardrail

The report tool uses:

```text
--minimum-total 250
```

If the result files only contain 2 or 11 tests, the tool fails the run.
