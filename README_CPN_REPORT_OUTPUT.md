# CPN Report Output

## Purpose

This document defines the report folders, file formats, and pipeline handoff points for CVIS reporting.

## Output folders

The authoritative local and pipeline run writes three output families:

```text
TestResults
├── TRX
│   └── **\*.trx
├── NUnitXml
│   └── **\*.xml
└── CPN
    ├── cpn-report.html
    ├── cpn-report.json
    ├── cpn-report-all-tests.html
    ├── cpn-report-all-tests.json
    ├── cpn-report-summary.txt
    └── Tests
        └── *.json
```

## Which output is used for what?

| Output | Consumer | Purpose |
|---|---|---|
| `TestResults\TRX\**\*.trx` | Visual Studio, Azure, artifact review | Standard Microsoft test result format |
| `TestResults\NUnitXml\**\*.xml` | HyperExecute `partialReports` | Framework parser input and test count |
| `TestResults\CPN\cpn-report.html` | Humans | Main readable CVIS report |
| `TestResults\CPN\cpn-report.json` | Tools | Main machine-readable CVIS report |
| `TestResults\CPN\cpn-report-all-tests.html` | Humans | Explicit all-tests readable report alias |
| `TestResults\CPN\cpn-report-all-tests.json` | Tools | Explicit all-tests machine-readable alias |
| `TestResults\CPN\cpn-report-summary.txt` | Console/artifact summary | Totals and source summary |
| `TestResults\CPN\Tests\*.json` | Tools/debugging | Per-test detail files |

## Correct local command

Run this from the solution root:

```powershell
.\scripts\run-cvis-authoritative-report-local.ps1 -Configuration Debug -MinimumTotal 250
```

The script runs every discovered `*.Tests.csproj`, writes TRX and NUnit XML, then builds the CVIS report from those outputs.

## Manual report-tool command

```powershell
dotnet run --project .\CVIS.Playwright.Reporting.Tool\CVIS.Playwright.Reporting.Tool.csproj -- `
  --trx-root .\TestResults\TRX `
  --nunit-xml-root .\TestResults\NUnitXml `
  --output-root .\TestResults\CPN `
  --framework-name "CVIS Authoritative Test Run" `
  --minimum-total 250
```

## Pipeline requirement

The pipeline must parse NUnit XML, not the CPN HTML file:

```yaml
report: true
partialReports:
  type: nunit
  location: .\TestResults\NUnitXml
  frameworkName: nunit
```

The pipeline must upload all three folders:

```yaml
mergeArtifacts: true
uploadArtefacts:
  - name: cvis-authoritative-test-output
    path:
      - .\TestResults\NUnitXml
      - .\TestResults\TRX
      - .\TestResults\CPN
```

## Required pipeline checks

Fail the pipeline if any required format is missing:

```text
TestResults\TRX\**\*.trx
TestResults\NUnitXml\**\*.xml
TestResults\CPN\cpn-report.html
TestResults\CPN\cpn-report.json
TestResults\CPN\cpn-report-all-tests.html
TestResults\CPN\cpn-report-all-tests.json
TestResults\CPN\cpn-report-summary.txt
TestResults\CPN\Tests\*.json
```

## Important distinction

`cpn-report.html` is the authoritative CVIS human report generated from TRX and NUnit XML.

`cpn-lifecycle-report.html` is diagnostic lifecycle output only and must not be used as the full test count.
