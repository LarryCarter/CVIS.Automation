# CPN Report Output

## Why you only saw the NUnit folder

This command creates NUnit/TRX output:

```powershell
dotnet test .\CVIS.Playwright.NUnitCompat.Tests\CVIS.Playwright.NUnitCompat.Tests.csproj ^
  --logger "trx;LogFileName=cpn-tests.trx" ^
  --results-directory ".\TestResults\NUnit" ^
  -- NUnit.TestOutputXml=.\TestResults\NUnitXml
```

That creates:

```text
TestResults\NUnit
TestResults\NUnitXml
```

It does not guarantee:

```text
TestResults\CPN
```

unless CPN reporting is enabled and the CPN report root is set.

## Correct local command

Run this from the solution root:

```powershell
set CPN_REPORT_ENABLED=true
set CPN_REPORT_ROOT=%CD%\TestResults\CPN

dotnet test .\CVIS.Playwright.NUnitCompat.Tests\CVIS.Playwright.NUnitCompat.Tests.csproj ^
  --logger "trx;LogFileName=cpn-tests.trx" ^
  --results-directory ".\TestResults\NUnit" ^
  -- NUnit.TestOutputXml=.\TestResults\NUnitXml
```

Expected folders:

```text
TestResults
├── NUnitXml
│   └── *.xml
├── NUnit
│   └── cpn-tests.trx
└── CPN
    ├── cpn-report.html
    ├── cpn-report.json
    └── Tests
        └── *.json
```

## Easier local scripts

```powershell
.\scripts\run-cpn-reporting-local.ps1
```

```powershell
.\scripts\run-cvis-automation-reporting-local.ps1
```

## Important

CPN reports are only created for tests that inherit from CPN base classes:

```csharp
CVISPlaywrightTest
CVISBrowserTest
CVISContextTest
CVISPageTest
CVISApiTest
```

Plain NUnit tests still appear in NUnit/TRX/XML, but they do not appear in the CPN HTML report.

## HyperExecute sample YAML

```yaml
version: "0.1"
runson: win

autosplit: false
concurrency: 1
testRunnerExecutor: cmd
workingDirectory: .

env:
  CPN_REPORT_ENABLED: "true"
  CPN_REPORT_ROOT: ".\\TestResults\\CPN"

pre:
  - if exist .\\TestResults rmdir /s /q .\\TestResults
  - dotnet restore .\\CVIS.Playwright.NUnitCompat.Tests\\CVIS.Playwright.NUnitCompat.Tests.csproj
  - dotnet build .\\CVIS.Playwright.NUnitCompat.Tests\\CVIS.Playwright.NUnitCompat.Tests.csproj --no-restore

testSuites:
  - dotnet test .\\CVIS.Playwright.NUnitCompat.Tests\\CVIS.Playwright.NUnitCompat.Tests.csproj --no-build --logger "trx;LogFileName=cpn-tests.trx" --results-directory ".\\TestResults\\NUnit" -- NUnit.TestOutputXml=.\\TestResults\\NUnitXml

report: true
partialReports:
  type: nunit
  location: .\\TestResults\\NUnitXml
  frameworkName: nunit

mergeArtifacts: true
uploadArtefacts:
  - name: cpn-test-output
    path:
      - .\\TestResults\\NUnitXml
      - .\\TestResults\\NUnit
      - .\\TestResults\\CPN
```

## Which folder goes where?

```text
HyperExecute report parser:
  TestResults\NUnitXml

Visual Studio / Azure / dotnet artifact:
  TestResults\NUnit

CPN human report:
  TestResults\CPN\cpn-report.html

CPN machine report:
  TestResults\CPN\cpn-report.json
```
