# Functional Test Reporting

# Purpose

This folder contains lifecycle diagnostic reporting for CVIS functional tests.

# Responsibilities

- Record setup, teardown, outcome, duration, and diagnostic details from tests that pass through CVIS lifecycle hooks.
- Support lifecycle debugging.
- Keep lifecycle diagnostics separate from authoritative test-run reporting.

# When to use

Use this folder when diagnosing fixture or test lifecycle behavior.

# When NOT to use

Do not use lifecycle diagnostics as the authoritative test total.

# Architecture

The authoritative test report is generated from real NUnit/TRX outputs, not from lifecycle logs.

Authoritative input folders:

```text
TestResults\TRX
TestResults\NUnitXml
```

Authoritative CVIS outputs:

```text
TestResults\CPN\cpn-report.html
TestResults\CPN\cpn-report.json
TestResults\CPN\cpn-report-all-tests.html
TestResults\CPN\cpn-report-all-tests.json
TestResults\CPN\cpn-report-summary.txt
TestResults\CPN\Tests\*.json
```

Lifecycle report:

```text
TestResults\CPN\cpn-lifecycle-report.html
```

# Examples

Local full run:

```powershell
.\scripts\run-cvis-authoritative-report-local.ps1 -Configuration Debug -MinimumTotal 250
```

# Pipeline

The pipeline parser must use:

```text
TestResults\NUnitXml
```

The pipeline artifacts must include:

```text
TestResults\TRX
TestResults\NUnitXml
TestResults\CPN
```

# Common mistakes

- Counting `cpn-lifecycle-report.html` as if it represents every discovered NUnit test.
- Assuming tests that do not inherit CVIS base classes will appear in lifecycle diagnostics.
- Uploading CPN artifacts while forgetting that the pipeline parser reads NUnit XML.

# Related folders

- `CVIS.Playwright.Reporting`
- `CVIS.Playwright.Reporting.Tool`
- `scripts`
