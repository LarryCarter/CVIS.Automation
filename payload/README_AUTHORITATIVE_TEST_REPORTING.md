# Hard Fix: Authoritative All Tests Report

The old HTML was a CPN lifecycle report. It measured teardown on tests that directly inherited from CPN base classes, so it could show 2 tests while Visual Studio showed hundreds or thousands.

The new authoritative report is built from the actual test runner outputs:

```text
TestResults\TRX
TestResults\NUnitXml
```

Run:

```powershell
.\scripts\run-authoritative-test-report-local.ps1
```

Open:

```text
TestResults\CPN\cpn-report.html
```

HyperExecute should parse:

```text
TestResults\NUnitXml
```

using:

```yaml
report: true
partialReports:
  type: nunit
  location: .\TestResults\NUnitXml
  frameworkName: nunit
```

The script fails if fewer than 250 tests are found, so it will not silently submit a 2-test report.
