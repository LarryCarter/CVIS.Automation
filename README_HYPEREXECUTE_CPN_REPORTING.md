# HyperExecute CPN Reporting

## Output folders

```text
TestResults
├── NUnitXml
│   └── *.xml
├── NUnit
│   └── *.trx
└── CPN
    ├── cpn-report.html
    ├── cpn-report.json
    └── Tests
        └── *.json
```

## HyperExecute parsed report

HyperExecute should parse:

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

## CPN artifact report

```yaml
uploadArtefacts:
  - name: cpn-test-output
    path:
      - .\TestResults\NUnitXml
      - .\TestResults\NUnit
      - .\TestResults\CPN
```

## Required environment variables

```yaml
env:
  CPN_REPORT_ENABLED: "true"
  CPN_REPORT_ROOT: ".\TestResults\CPN"
```

Local cmd:

```powershell
set CPN_REPORT_ENABLED=true
set CPN_REPORT_ROOT=%CD%\TestResults\CPN
```

## Local command

```powershell
set CPN_REPORT_ENABLED=true
set CPN_REPORT_ROOT=%CD%\TestResults\CPN

dotnet test .\CVIS.Playwright.NUnitCompat.Tests\CVIS.Playwright.NUnitCompat.Tests.csproj ^
  --logger "trx;LogFileName=cpn-tests.trx" ^
  --results-directory ".\TestResults\NUnit" ^
  -- NUnit.TestOutputXml=.\TestResults\NUnitXml
```

## Local scripts

```powershell
.\scripts\run-cpn-reporting-local.ps1
.\scripts\run-cvis-automation-reporting-local.ps1
```

## Important

NUnit XML contains all NUnit tests.

CPN HTML/JSON contains only tests that use CPN base classes.

That is intentional. HyperExecute gets the full framework test count from NUnit XML, while the CPN report gives detailed CPN-owned reporting for tests running through the CPN layer.
