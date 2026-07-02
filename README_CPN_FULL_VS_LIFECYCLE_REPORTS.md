# CPN Full vs Lifecycle Reports

## Open this report for all tests

```text
TestResults\CPN\cpn-report.html
```

That report is generated from TRX plus NUnit XML after `dotnet test`, so it represents the authoritative test run.

Machine-readable equivalent:

```text
TestResults\CPN\cpn-report.json
```

All-tests aliases:

```text
TestResults\CPN\cpn-report-all-tests.html
TestResults\CPN\cpn-report-all-tests.json
```

Summary and per-test detail:

```text
TestResults\CPN\cpn-report-summary.txt
TestResults\CPN\Tests\*.json
```

## Lifecycle-only report

```text
TestResults\CPN\cpn-lifecycle-report.html
```

That report only reflects lifecycle diagnostics. It must not be used as the authoritative test count.

## Run the full automation report

```powershell
.\scripts\run-cvis-authoritative-report-local.ps1 -Configuration Debug -MinimumTotal 250
```

Then open:

```text
TestResults\CPN\cpn-report.html
```

## Pipeline pattern

Use:

```text
hyperexecute-cvis-authoritative-nunit.yaml
```

The pipeline should parse NUnit XML:

```yaml
report: true
partialReports:
  type: nunit
  location: .\TestResults\NUnitXml
  frameworkName: nunit
```

The pipeline should upload all report families:

```yaml
mergeArtifacts: true
uploadArtefacts:
  - name: cvis-authoritative-test-output
    path:
      - .\TestResults\NUnitXml
      - .\TestResults\TRX
      - .\TestResults\CPN
```

## Required checks

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
