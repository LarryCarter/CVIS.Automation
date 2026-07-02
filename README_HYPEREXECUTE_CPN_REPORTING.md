# HyperExecute CPN Reporting

## Purpose

This document explains how HyperExecute consumes the CVIS test outputs and how the pipeline proves the report package was written.

## Output folders

```text
TestResults
├── NUnitXml
│   └── **\*.xml
├── TRX
│   └── **\*.trx
└── CPN
    ├── cpn-report.html
    ├── cpn-report.json
    ├── cpn-report-all-tests.html
    ├── cpn-report-all-tests.json
    ├── cpn-report-summary.txt
    └── Tests
        └── *.json
```

## HyperExecute parsed report

HyperExecute should parse NUnit XML:

```text
TestResults\NUnitXml
```

```yaml
report: true
partialReports:
  type: nunit
  location: .\TestResults\NUnitXml
  frameworkName: nunit
```

That is the pipeline parser input and the framework test-count source.

## CVIS artifact report

The CVIS report package is uploaded as artifacts:

```yaml
mergeArtifacts: true
uploadArtefacts:
  - name: cvis-authoritative-test-output
    path:
      - .\TestResults\NUnitXml
      - .\TestResults\TRX
      - .\TestResults\CPN
```

## Local command

```powershell
.\scripts\run-cvis-authoritative-report-local.ps1 -Configuration Debug -MinimumTotal 250
```

## Pipeline command

The HyperExecute YAML runs the same authoritative script:

```yaml
testSuites:
  - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run-cvis-authoritative-report-local.ps1
```

## Required output checks

The pipeline `post` section should fail if any required output is missing:

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

## Important

`cpn-report.html` and `cpn-report.json` are generated from TRX plus NUnit XML after the run. They are the authoritative CVIS report outputs.

`cpn-lifecycle-report.html` is diagnostic lifecycle output only. Do not use it as the full test count.
