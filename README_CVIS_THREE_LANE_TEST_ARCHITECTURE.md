# CVIS Three-Lane NUnit / HyperExecute Test Architecture

## Goal

NUnit is the spine.

The team must be able to write:

1. Plain NUnit functional tests
2. Playwright browser tests only where browser automation makes sense
3. Shared infrastructure that does not force Playwright into every test

## Lane 1 — Pure Functional NUnit Tests

Project/library:

```text
CVIS.FunctionalTesting
```

Base class:

```csharp
BaseFunctionalTest
```

Use this for:

```text
PolicyDrift
API tests
database tests
config tests
file validation
service/logic tests
```

This lane has no Playwright dependency.

## Lane 2 — Playwright Browser NUnit Tests

Project/library:

```text
CVIS.Playwright.NUnitCompat
```

Base classes:

```csharp
CVISPlaywrightTest
CVISPageTest
```

Use this only when a browser is actually required.

## Lane 3 — Authoritative Reporting

Projects:

```text
CVIS.Playwright.Reporting
CVIS.Playwright.Reporting.Tool
```

The authoritative report is generated after `dotnet test` from:

```text
TestResults\TRX
TestResults\NUnitXml
```

It writes:

```text
TestResults\CPN\cpn-report.html
TestResults\CPN\cpn-report.json
TestResults\CPN\cpn-report-summary.txt
```

The CPN lifecycle/teardown report is separate and should not be used for totals.

## Local Run

```powershell
.\scripts\run-cvis-authoritative-report-local.ps1
```

## HyperExecute

Use:

```text
hyperexecute-cvis-authoritative-nunit.yaml
```

HyperExecute parses:

```yaml
partialReports:
  type: nunit
  location: .\TestResults\NUnitXml
  frameworkName: nunit
```

The HTML is an artifact generated from the same TRX/NUnit XML result source.
