# CPN Full vs Lifecycle Reports

## Open this report for all tests

```text
TestResults\CPN\cpn-report.html
```

That report is generated from NUnit XML after `dotnet test`, so it includes all NUnit tests.

## Lifecycle-only report

```text
TestResults\CPN\cpn-lifecycle-report.html
```

That report only includes tests that directly inherit from CPN base classes.

## Run the full automation report

```powershell
.\scripts\run-cvis-automation-reporting-local.ps1
```

Then open:

```text
TestResults\CPN\cpn-report.html
```

## HyperExecute sample

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
