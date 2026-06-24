# CPN Full NUnit Report Bridge

## Why the CPN report only showed 2 tests

The lifecycle CPN report records tests that inherit from CPN base classes:

```csharp
CVISPlaywrightTest
CVISBrowserTest
CVISContextTest
CVISPageTest
CVISApiTest
```

Most existing tests are plain NUnit automation tests. They appear in Visual Studio and NUnit XML/TRX, but they are not recorded through the CPN lifecycle.

## Fix

This bridge parses NUnit XML after the test run and generates a full CPN-style report containing all NUnit tests.

## Full report output

```text
TestResults\CPN\cpn-report.html
TestResults\CPN\cpn-report.json
TestResults\CPN\cpn-report-all-tests.html
TestResults\CPN\cpn-report-all-tests.json
TestResults\CPN\Tests\*.json
```

## Local command

```powershell
.\scripts\run-cvis-automation-reporting-local.ps1
```

For CPN-only tests:

```powershell
.\scripts\run-cpn-reporting-local.ps1
```

## Manual command sequence

```powershell
$env:CPN_REPORT_ENABLED = "true"
$env:CPN_REPORT_ROOT = "$PWD\TestResults\CPN"

dotnet test .\CVIS.Automation.Tests\CVIS.Automation.Tests.csproj `
  --logger "trx;LogFileName=cvis-automation-tests.trx" `
  --results-directory ".\TestResults\NUnit" `
  -- NUnit.TestOutputXml=.\TestResults\NUnitXml

powershell -ExecutionPolicy Bypass -File .\scripts\merge-nunitxml-into-cpn-report.ps1 `
  -NUnitXmlRoot ".\TestResults\NUnitXml" `
  -CpnRoot ".\TestResults\CPN" `
  -FrameworkName "CVIS.Automation.Tests"
```

## HyperExecute YAML sample

```yaml
version: "0.1"
runson: win

autosplit: false
concurrency: 1
testRunnerExecutor: cmd
workingDirectory: .

env:
  CPN_REPORT_ENABLED: "true"
  CPN_REPORT_ROOT: ".\TestResults\CPN"

pre:
  - if exist .\TestResults rmdir /s /q .\TestResults
  - dotnet restore .\CVIS.Automation.Tests\CVIS.Automation.Tests.csproj
  - dotnet build .\CVIS.Automation.Tests\CVIS.Automation.Tests.csproj --no-restore

testSuites:
  - dotnet test .\CVIS.Automation.Tests\CVIS.Automation.Tests.csproj --no-build --logger "trx;LogFileName=cvis-automation-tests.trx" --results-directory ".\TestResults\NUnit" -- NUnit.TestOutputXml=.\TestResults\NUnitXml

post:
  - powershell -ExecutionPolicy Bypass -File .\scripts\merge-nunitxml-into-cpn-report.ps1 -NUnitXmlRoot .\TestResults\NUnitXml -CpnRoot .\TestResults\CPN -FrameworkName CVIS.Automation.Tests

report: true
partialReports:
  type: nunit
  location: .\TestResults\NUnitXml
  frameworkName: nunit

mergeArtifacts: true
uploadArtefacts:
  - name: cvis-test-output
    path:
      - .\TestResults\NUnitXml
      - .\TestResults\NUnit
      - .\TestResults\CPN
```
