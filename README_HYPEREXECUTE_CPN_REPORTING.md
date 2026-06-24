# HyperExecute CPN Reporting

## Purpose

This repo produces two kinds of output for HyperExecute:

1. **Framework report output** for HyperExecute to parse.
2. **CPN report artifacts** for humans and downstream tooling.

HyperExecute report generation is enabled with:

```yaml
report: true
partialReports:
```

## Output folders

```text
TestResults\\
  NUnitXml\\
    *.xml
  NUnit\\
    *.trx
  CPN\\
    cpn-report.html
    cpn-report.json
    Tests\\
      *.json
```

## HyperExecute parsed report

HyperExecute should parse the NUnit XML folder:

```text
TestResults\\NUnitXml
```

It is produced by the NUnit3 test adapter using:

```powershell
-- NUnit.TestOutputXml=.\TestResults\NUnitXml
```

YAML:

```yaml
report: true
partialReports:
  type: nunit
  location: .\TestResults\NUnitXml
  frameworkName: nunit
```

## CPN artifact report

CPN writes:

```text
TestResults\CPN\cpn-report.html
TestResults\CPN\cpn-report.json
TestResults\CPN\Tests\*.json
```

HyperExecute uploads it using:

```yaml
uploadArtefacts:
  - name: cpn-test-output
    path:
      - .\TestResults\NUnitXml
      - .\TestResults\NUnit
      - .\TestResults\CPN
```

## Local validation command

Run this from the solution root:

```powershell
set CPN_REPORT_ENABLED=true
set CPN_REPORT_ROOT=.\TestResults\CPN

dotnet test .\CVIS.Playwright.NUnitCompat.Tests\CVIS.Playwright.NUnitCompat.Tests.csproj ^
  --logger "trx;LogFileName=cpn-tests.trx" ^
  --results-directory ".\TestResults\NUnit" ^
  -- NUnit.TestOutputXml=.\TestResults\NUnitXml
```

Verify:

```powershell
dir .\TestResults\NUnitXml
dir .\TestResults\NUnit
dir .\TestResults\CPN
```

## HyperExecute YAML files

```text
hyperexecute-cpn-reporting.yaml
hyperexecute-cvis-automation-reporting.yaml
```

## HyperExecute run command

```powershell
hyperexecute.exe --user %LT_USERNAME% --key %LT_ACCESS_KEY% --config .\hyperexecute-cpn-reporting.yaml --download-report --download-artifacts
```

```powershell
hyperexecute.exe --user %LT_USERNAME% --key %LT_ACCESS_KEY% --config .\hyperexecute-cvis-automation-reporting.yaml --download-report --download-artifacts
```

## Important

HyperExecute gets its parsed report from NUnit XML.

The CPN HTML/JSON report is uploaded as an artifact.
