# Functional Test Reporting

# Purpose

This folder contains lifecycle diagnostic reporting for CVIS functional tests.

# Responsibilities

- Record setup, teardown, outcome, duration, and diagnostic details from tests that pass through CVIS lifecycle hooks.
- Support lifecycle debugging.

# When to use

Use this folder when diagnosing fixture or test lifecycle behavior.

# When NOT to use

Do not use lifecycle diagnostics as the authoritative test total.

# Architecture

The authoritative test report is generated from real NUnit/TRX outputs, not from lifecycle logs.

Authoritative report:

```text
TestResults\CPN\cpn-report.html
```

Lifecycle report:

```text
TestResults\CPN\cpn-lifecycle-report.html
```

# Examples

Local full run:

```powershell
.\scripts\run-cvis-authoritative-report-local.ps1
```

# Common mistakes

- Counting `cpn-lifecycle-report.html` as if it represents every discovered NUnit test.
- Assuming tests that do not inherit CVIS base classes will appear in lifecycle diagnostics.

# Related folders

- `CVIS.Playwright.Reporting`
- `CVIS.Playwright.Reporting.Tool`
- `scripts`
