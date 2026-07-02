# Scripts

# Purpose

This folder contains local automation commands for running CVIS tests and generating reports.

# Responsibilities

- Run real NUnit test execution.
- Write TRX and NUnit XML results.
- Generate the authoritative CVIS HTML and JSON reports.
- Fail locally or in the pipeline when required report outputs are missing.

# When to use

Use this folder when running local full test/report workflows.

# When NOT to use

Do not use scripts here as substitutes for test code. Do not use lifecycle-only output as the full report.

# Architecture

Local full run:

```powershell
.\scripts\run-cvis-authoritative-report-local.ps1
```

The script discovers `*.Tests.csproj` projects, writes TRX and NUnit XML output, then calls `CVIS.Playwright.Reporting.Tool` to build the authoritative CPN report.

Required output folders:

```text
TestResults\TRX
TestResults\NUnitXml
TestResults\CPN
```

Required output files:

```text
TestResults\CPN\cpn-report.html
TestResults\CPN\cpn-report.json
TestResults\CPN\cpn-report-all-tests.html
TestResults\CPN\cpn-report-all-tests.json
TestResults\CPN\cpn-report-summary.txt
TestResults\CPN\Tests\*.json
```

Pipeline parser input:

```text
TestResults\NUnitXml\**\*.xml
```

Human report:

```text
TestResults\CPN\cpn-report.html
```

Machine-readable report:

```text
TestResults\CPN\cpn-report.json
```

# Examples

```powershell
.\scripts\run-cvis-authoritative-report-local.ps1 -Configuration Debug -MinimumTotal 250
```

Manual pipeline-equivalent check after the script runs:

```powershell
Test-Path .\TestResults\CPN\cpn-report.html
Test-Path .\TestResults\CPN\cpn-report.json
Test-Path .\TestResults\CPN\cpn-report-summary.txt
Get-ChildItem .\TestResults\NUnitXml -Recurse -Filter *.xml
Get-ChildItem .\TestResults\TRX -Recurse -Filter *.trx
Get-ChildItem .\TestResults\CPN\Tests -Recurse -Filter *.json
```

# Pipeline

`hyperexecute-cvis-authoritative-nunit.yaml` runs the authoritative script, points HyperExecute at `TestResults\NUnitXml`, uploads TRX/NUnitXml/CPN as artifacts, and fails in `post` if any required report file is missing.

# Common mistakes

- Running one test project manually and comparing that count to the full report.
- Looking at `cpn-lifecycle-report.html` for authoritative totals.
- Uploading `TestResults\CPN` but forgetting to point the pipeline parser at `TestResults\NUnitXml`.
- Generating TRX/XML without running the report tool that writes `cpn-report.html` and `cpn-report.json`.

# Related folders

- `CVIS.Playwright.Reporting.Tool`
- `CVIS.Playwright.Reporting`
- `CVIS.Automation.Tests`
- `CVIS.Playwright.NUnitCompat.Tests`
