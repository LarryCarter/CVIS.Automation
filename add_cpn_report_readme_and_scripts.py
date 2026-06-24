from pathlib import Path

ROOT = Path.cwd()

def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")

def main() -> None:
    write(ROOT / "scripts" / "run-cpn-reporting-local.ps1", '''
param([string]$Configuration = "Debug")

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$TestResults = Join-Path $Root "TestResults"
$CpnResults = Join-Path $TestResults "CPN"
$NUnitResults = Join-Path $TestResults "NUnit"
$NUnitXmlResults = Join-Path $TestResults "NUnitXml"

if (Test-Path $TestResults) {
    Remove-Item $TestResults -Recurse -Force
}

New-Item -ItemType Directory -Force -Path $CpnResults | Out-Null
New-Item -ItemType Directory -Force -Path $NUnitResults | Out-Null
New-Item -ItemType Directory -Force -Path $NUnitXmlResults | Out-Null

$env:CPN_REPORT_ENABLED = "true"
$env:CPN_REPORT_ROOT = $CpnResults

dotnet test "$Root\\CVIS.Playwright.NUnitCompat.Tests\\CVIS.Playwright.NUnitCompat.Tests.csproj" `
    --configuration $Configuration `
    --logger "trx;LogFileName=cpn-tests.trx" `
    --results-directory "$NUnitResults" `
    -- NUnit.TestOutputXml="$NUnitXmlResults"

Write-Host ""
Write-Host "Expected output:"
Write-Host "  $NUnitXmlResults"
Write-Host "  $NUnitResults"
Write-Host "  $CpnResults"
Write-Host ""
Write-Host "Open CPN HTML report:"
Write-Host "  $CpnResults\\cpn-report.html"
''')

    write(ROOT / "scripts" / "run-cvis-automation-reporting-local.ps1", '''
param([string]$Configuration = "Debug")

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$TestResults = Join-Path $Root "TestResults"
$CpnResults = Join-Path $TestResults "CPN"
$NUnitResults = Join-Path $TestResults "NUnit"
$NUnitXmlResults = Join-Path $TestResults "NUnitXml"

if (Test-Path $TestResults) {
    Remove-Item $TestResults -Recurse -Force
}

New-Item -ItemType Directory -Force -Path $CpnResults | Out-Null
New-Item -ItemType Directory -Force -Path $NUnitResults | Out-Null
New-Item -ItemType Directory -Force -Path $NUnitXmlResults | Out-Null

$env:CPN_REPORT_ENABLED = "true"
$env:CPN_REPORT_ROOT = $CpnResults

dotnet test "$Root\\CVIS.Automation.Tests\\CVIS.Automation.Tests.csproj" `
    --configuration $Configuration `
    --logger "trx;LogFileName=cvis-automation-tests.trx" `
    --results-directory "$NUnitResults" `
    -- NUnit.TestOutputXml="$NUnitXmlResults"

Write-Host ""
Write-Host "Expected output:"
Write-Host "  $NUnitXmlResults"
Write-Host "  $NUnitResults"
Write-Host "  $CpnResults"
Write-Host ""
Write-Host "Note: CPN report files only include tests that inherit from CPN base classes."
''')

    write(ROOT / "README_CPN_REPORT_OUTPUT.md", '''
# CPN Report Output

## Why you only saw the NUnit folder

This command creates NUnit/TRX output:

```powershell
dotnet test .\\CVIS.Playwright.NUnitCompat.Tests\\CVIS.Playwright.NUnitCompat.Tests.csproj ^
  --logger "trx;LogFileName=cpn-tests.trx" ^
  --results-directory ".\\TestResults\\NUnit" ^
  -- NUnit.TestOutputXml=.\\TestResults\\NUnitXml
```

That creates:

```text
TestResults\\NUnit
TestResults\\NUnitXml
```

It does not guarantee:

```text
TestResults\\CPN
```

unless CPN reporting is enabled and the CPN report root is set.

## Correct local command

Run this from the solution root:

```powershell
set CPN_REPORT_ENABLED=true
set CPN_REPORT_ROOT=%CD%\\TestResults\\CPN

dotnet test .\\CVIS.Playwright.NUnitCompat.Tests\\CVIS.Playwright.NUnitCompat.Tests.csproj ^
  --logger "trx;LogFileName=cpn-tests.trx" ^
  --results-directory ".\\TestResults\\NUnit" ^
  -- NUnit.TestOutputXml=.\\TestResults\\NUnitXml
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
.\\scripts\\run-cpn-reporting-local.ps1
```

```powershell
.\\scripts\\run-cvis-automation-reporting-local.ps1
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
  CPN_REPORT_ROOT: ".\\\\TestResults\\\\CPN"

pre:
  - if exist .\\\\TestResults rmdir /s /q .\\\\TestResults
  - dotnet restore .\\\\CVIS.Playwright.NUnitCompat.Tests\\\\CVIS.Playwright.NUnitCompat.Tests.csproj
  - dotnet build .\\\\CVIS.Playwright.NUnitCompat.Tests\\\\CVIS.Playwright.NUnitCompat.Tests.csproj --no-restore

testSuites:
  - dotnet test .\\\\CVIS.Playwright.NUnitCompat.Tests\\\\CVIS.Playwright.NUnitCompat.Tests.csproj --no-build --logger "trx;LogFileName=cpn-tests.trx" --results-directory ".\\\\TestResults\\\\NUnit" -- NUnit.TestOutputXml=.\\\\TestResults\\\\NUnitXml

report: true
partialReports:
  type: nunit
  location: .\\\\TestResults\\\\NUnitXml
  frameworkName: nunit

mergeArtifacts: true
uploadArtefacts:
  - name: cpn-test-output
    path:
      - .\\\\TestResults\\\\NUnitXml
      - .\\\\TestResults\\\\NUnit
      - .\\\\TestResults\\\\CPN
```

## Which folder goes where?

```text
HyperExecute report parser:
  TestResults\\NUnitXml

Visual Studio / Azure / dotnet artifact:
  TestResults\\NUnit

CPN human report:
  TestResults\\CPN\\cpn-report.html

CPN machine report:
  TestResults\\CPN\\cpn-report.json
```
''')

    write(ROOT / "README_HYPEREXECUTE_CPN_REPORTING.md", '''
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
TestResults\\NUnitXml
```

```yaml
report: true
partialReports:
  type: nunit
  location: .\\TestResults\\NUnitXml
  frameworkName: nunit
```

## CPN artifact report

```yaml
uploadArtefacts:
  - name: cpn-test-output
    path:
      - .\\TestResults\\NUnitXml
      - .\\TestResults\\NUnit
      - .\\TestResults\\CPN
```

## Required environment variables

```yaml
env:
  CPN_REPORT_ENABLED: "true"
  CPN_REPORT_ROOT: ".\\TestResults\\CPN"
```

Local cmd:

```powershell
set CPN_REPORT_ENABLED=true
set CPN_REPORT_ROOT=%CD%\\TestResults\\CPN
```

## Local command

```powershell
set CPN_REPORT_ENABLED=true
set CPN_REPORT_ROOT=%CD%\\TestResults\\CPN

dotnet test .\\CVIS.Playwright.NUnitCompat.Tests\\CVIS.Playwright.NUnitCompat.Tests.csproj ^
  --logger "trx;LogFileName=cpn-tests.trx" ^
  --results-directory ".\\TestResults\\NUnit" ^
  -- NUnit.TestOutputXml=.\\TestResults\\NUnitXml
```

## Local scripts

```powershell
.\\scripts\\run-cpn-reporting-local.ps1
.\\scripts\\run-cvis-automation-reporting-local.ps1
```

## Important

NUnit XML contains all NUnit tests.

CPN HTML/JSON contains only tests that use CPN base classes.

That is intentional. HyperExecute gets the full framework test count from NUnit XML, while the CPN report gives detailed CPN-owned reporting for tests running through the CPN layer.
''')

    print("Added CPN report README and local reporting scripts.")

if __name__ == "__main__":
    main()
