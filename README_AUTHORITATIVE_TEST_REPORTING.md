# Authoritative Test Reporting

## Purpose

This document explains which files prove the tests ran, which files feed the pipeline parser, and which files are uploaded for human and machine review.

## Correct source of truth

The authoritative source of truth is the actual test runner output:

```text
TestResults\TRX
TestResults\NUnitXml
```

The CVIS HTML/JSON reports are generated after `dotnet test` from those result files.

## Local run

```powershell
.\scripts\run-cvis-authoritative-report-local.ps1
```

The script does three things:

1. Discovers test projects ending in `.Tests.csproj`.
2. Runs `dotnet test` for each project and writes TRX plus NUnit XML.
3. Runs `CVIS.Playwright.Reporting.Tool` to generate the CVIS report package.

## Output formats

| Output | Path | Purpose |
|---|---|---|
| TRX | `TestResults\TRX\**\*.trx` | Visual Studio, Azure, and runner-compatible test output |
| NUnit XML | `TestResults\NUnitXml\**\*.xml` | HyperExecute parser input and framework test count |
| CVIS HTML | `TestResults\CPN\cpn-report.html` | Main human-readable authoritative report |
| CVIS JSON | `TestResults\CPN\cpn-report.json` | Main machine-readable authoritative report |
| All-tests HTML alias | `TestResults\CPN\cpn-report-all-tests.html` | Explicit all-tests human report alias |
| All-tests JSON alias | `TestResults\CPN\cpn-report-all-tests.json` | Explicit all-tests machine report alias |
| Summary text | `TestResults\CPN\cpn-report-summary.txt` | Console/artifact summary of totals |
| Per-test JSON | `TestResults\CPN\Tests\*.json` | One JSON file per test case |

The reporting tool writes these CVIS files from `TRX+NUnitXml` and records that source in the report summary.

## Report tool command

The local script calls the report tool like this:

```powershell
dotnet run --project .\CVIS.Playwright.Reporting.Tool\CVIS.Playwright.Reporting.Tool.csproj -- `
  --trx-root .\TestResults\TRX `
  --nunit-xml-root .\TestResults\NUnitXml `
  --output-root .\TestResults\CPN `
  --framework-name "CVIS Authoritative Test Run" `
  --minimum-total 250
```

`--minimum-total` is a guardrail. If the result files only contain a small partial run, the report tool fails instead of producing a misleading report.

## Pipeline requirements

Use:

```text
hyperexecute-cvis-authoritative-nunit.yaml
```

The pipeline must:

1. Delete old `TestResults` before the run.
2. Run `scripts\run-cvis-authoritative-report-local.ps1`.
3. Point the HyperExecute parser at `TestResults\NUnitXml`.
4. Upload `TestResults\NUnitXml`, `TestResults\TRX`, and `TestResults\CPN` as artifacts.
5. Fail the run if any required report output is missing.

Parser configuration:

```yaml
report: true
partialReports:
  type: nunit
  location: .\TestResults\NUnitXml
  frameworkName: nunit
```

Artifact configuration:

```yaml
mergeArtifacts: true
uploadArtefacts:
  - name: cvis-authoritative-test-output
    path:
      - .\TestResults\NUnitXml
      - .\TestResults\TRX
      - .\TestResults\CPN
```

## Required pipeline file checks

The pipeline should fail if any of these are missing:

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

## Lifecycle report

The lifecycle report is intentionally separate:

```text
TestResults\CPN\cpn-lifecycle-report.html
```

It is diagnostic only. Do not use it as the full test count and do not submit it as the authoritative pipeline report.
