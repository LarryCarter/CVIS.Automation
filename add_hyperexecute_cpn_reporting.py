r"""
CVIS RDEL Update Script
Package: Add HyperExecute CPN Reporting
"""
from pathlib import Path

ROOT = Path.cwd()

def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")

def main() -> None:
    write(ROOT / "hyperexecute-cpn-reporting.yaml", """
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
  - dotnet restore .\\\\CVIS.Playwright.Automation.Shared\\\\CVIS.Playwright.Automation.Shared.csproj
  - dotnet restore .\\\\CVIS.Playwright.NUnitCompat\\\\CVIS.Playwright.NUnitCompat.csproj
  - dotnet restore .\\\\CVIS.Playwright.NUnitCompat.Tests\\\\CVIS.Playwright.NUnitCompat.Tests.csproj
  - dotnet build .\\\\CVIS.Playwright.Automation.Shared\\\\CVIS.Playwright.Automation.Shared.csproj --no-restore
  - dotnet build .\\\\CVIS.Playwright.NUnitCompat\\\\CVIS.Playwright.NUnitCompat.csproj --no-restore
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
""")

    write(ROOT / "hyperexecute-cvis-automation-reporting.yaml", """
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
  - dotnet restore .\\\\CVIS.Playwright.Automation.Shared\\\\CVIS.Playwright.Automation.Shared.csproj
  - dotnet restore .\\\\CVIS.Playwright.NUnitCompat\\\\CVIS.Playwright.NUnitCompat.csproj
  - dotnet restore .\\\\CVIS.Automation.Tests\\\\CVIS.Automation.Tests.csproj
  - dotnet build .\\\\CVIS.Playwright.Automation.Shared\\\\CVIS.Playwright.Automation.Shared.csproj --no-restore
  - dotnet build .\\\\CVIS.Playwright.NUnitCompat\\\\CVIS.Playwright.NUnitCompat.csproj --no-restore
  - dotnet build .\\\\CVIS.Automation.Tests\\\\CVIS.Automation.Tests.csproj --no-restore

testSuites:
  - dotnet test .\\\\CVIS.Automation.Tests\\\\CVIS.Automation.Tests.csproj --no-build --logger "trx;LogFileName=cvis-automation-tests.trx" --results-directory ".\\\\TestResults\\\\NUnit" -- NUnit.TestOutputXml=.\\\\TestResults\\\\NUnitXml

report: true
partialReports:
  type: nunit
  location: .\\\\TestResults\\\\NUnitXml
  frameworkName: nunit

mergeArtifacts: true
uploadArtefacts:
  - name: cvis-automation-test-output
    path:
      - .\\\\TestResults\\\\NUnitXml
      - .\\\\TestResults\\\\NUnit
      - .\\\\TestResults\\\\CPN
""")

    write(ROOT / "README_HYPEREXECUTE_CPN_REPORTING.md", """
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
TestResults\\\\
  NUnitXml\\\\
    *.xml
  NUnit\\\\
    *.trx
  CPN\\\\
    cpn-report.html
    cpn-report.json
    Tests\\\\
      *.json
```

## HyperExecute parsed report

HyperExecute should parse the NUnit XML folder:

```text
TestResults\\\\NUnitXml
```

It is produced by the NUnit3 test adapter using:

```powershell
-- NUnit.TestOutputXml=.\\TestResults\\NUnitXml
```

YAML:

```yaml
report: true
partialReports:
  type: nunit
  location: .\\TestResults\\NUnitXml
  frameworkName: nunit
```

## CPN artifact report

CPN writes:

```text
TestResults\\CPN\\cpn-report.html
TestResults\\CPN\\cpn-report.json
TestResults\\CPN\\Tests\\*.json
```

HyperExecute uploads it using:

```yaml
uploadArtefacts:
  - name: cpn-test-output
    path:
      - .\\TestResults\\NUnitXml
      - .\\TestResults\\NUnit
      - .\\TestResults\\CPN
```

## Local validation command

Run this from the solution root:

```powershell
set CPN_REPORT_ENABLED=true
set CPN_REPORT_ROOT=.\\TestResults\\CPN

dotnet test .\\CVIS.Playwright.NUnitCompat.Tests\\CVIS.Playwright.NUnitCompat.Tests.csproj ^
  --logger "trx;LogFileName=cpn-tests.trx" ^
  --results-directory ".\\TestResults\\NUnit" ^
  -- NUnit.TestOutputXml=.\\TestResults\\NUnitXml
```

Verify:

```powershell
dir .\\TestResults\\NUnitXml
dir .\\TestResults\\NUnit
dir .\\TestResults\\CPN
```

## HyperExecute YAML files

```text
hyperexecute-cpn-reporting.yaml
hyperexecute-cvis-automation-reporting.yaml
```

## HyperExecute run command

```powershell
hyperexecute.exe --user %LT_USERNAME% --key %LT_ACCESS_KEY% --config .\\hyperexecute-cpn-reporting.yaml --download-report --download-artifacts
```

```powershell
hyperexecute.exe --user %LT_USERNAME% --key %LT_ACCESS_KEY% --config .\\hyperexecute-cvis-automation-reporting.yaml --download-report --download-artifacts
```

## Important

HyperExecute gets its parsed report from NUnit XML.

The CPN HTML/JSON report is uploaded as an artifact.
""")

    print("Added HyperExecute CPN reporting YAML and README.")

if __name__ == "__main__":
    main()
