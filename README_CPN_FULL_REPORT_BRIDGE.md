# CPN Full NUnit Report Bridge

## Purpose

The CVIS report bridge builds the human and machine-readable CVIS reports from real NUnit runner output.

## Source inputs

The bridge reads:

```text
TestResults\TRX\**\*.trx
TestResults\NUnitXml\**\*.xml
```

TRX and NUnit XML are produced by `dotnet test`. The reporting tool combines and deduplicates those entries into one authoritative CVIS report package.

## Full report output

```text
TestResults\CPN\cpn-report.html
TestResults\CPN\cpn-report.json
TestResults\CPN\cpn-report-all-tests.html
TestResults\CPN\cpn-report-all-tests.json
TestResults\CPN\cpn-report-summary.txt
TestResults\CPN\Tests\*.json
```

## Local command

```powershell
.\scripts\run-cvis-authoritative-report-local.ps1 -Configuration Debug -MinimumTotal 250
```

## Manual command sequence

```powershell
dotnet test .\CVIS.Automation.Tests\CVIS.Automation.Tests.csproj `
  --logger "trx;LogFileName=cvis-automation-tests.trx" `
  --results-directory ".\TestResults\TRX\CVIS.Automation.Tests" `
  -- NUnit.TestOutputXml=.\TestResults\NUnitXml\CVIS.Automation.Tests

dotnet run --project .\CVIS.Playwright.Reporting.Tool\CVIS.Playwright.Reporting.Tool.csproj -- `
  --trx-root .\TestResults\TRX `
  --nunit-xml-root .\TestResults\NUnitXml `
  --output-root .\TestResults\CPN `
  --framework-name "CVIS Authoritative Test Run" `
  --minimum-total 250
```

## HyperExecute YAML pattern

```yaml
testSuites:
  - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run-cvis-authoritative-report-local.ps1

report: true
partialReports:
  type: nunit
  location: .\TestResults\NUnitXml
  frameworkName: nunit

mergeArtifacts: true
uploadArtefacts:
  - name: cvis-authoritative-test-output
    path:
      - .\TestResults\NUnitXml
      - .\TestResults\TRX
      - .\TestResults\CPN
```

## Required pipeline checks

The pipeline should fail when any of these are missing:

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

## Lifecycle distinction

`cpn-lifecycle-report.html` is separate diagnostic output. The full report bridge does not rely on lifecycle-only counts.
