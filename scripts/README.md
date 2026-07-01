# Scripts

# Purpose

This folder contains local automation commands for running CVIS tests and generating reports.

# Responsibilities

- Run real NUnit test execution.
- Write TRX and NUnit XML results.
- Generate the authoritative CVIS HTML report.

# When to use

Use this folder when running local full test/report workflows.

# When NOT to use

Do not use scripts here as substitutes for test code. Do not use lifecycle-only output as the full report.

# Architecture

Local full run:

```powershell
.\scripts\run-cvis-authoritative-report-local.ps1
```

Outputs:

```text
TestResults\TRX
TestResults\NUnitXml
TestResults\CPN\cpn-report.html
```

# Examples

```powershell
.\scripts\run-cvis-authoritative-report-local.ps1 -Configuration Debug -MinimumTotal 250
```

# Common mistakes

- Running one test project manually and comparing that count to the full report.
- Looking at `cpn-lifecycle-report.html` for authoritative totals.

# Related folders

- `CVIS.Playwright.Reporting.Tool`
- `CVIS.Automation.Tests`
- `CVIS.Playwright.NUnitCompat.Tests`
