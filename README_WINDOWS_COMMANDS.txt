# Hard Restructure CPN Reporting

This package separates the reports correctly.

## Lifecycle report

```text
TestResults\CPN\cpn-lifecycle-report.html
```

Only CPN base-class teardown tests.

## Authoritative all-tests report

```text
TestResults\CPN\cpn-report.html
```

Generated from:

```text
TestResults\TRX
TestResults\NUnitXml
```

## After applying

Run:

```powershell
.\scripts\run-authoritative-test-report-local.ps1
```

Open:

```text
TestResults\CPN\cpn-report.html
```

## HyperExecute

Use:

```text
hyperexecute-authoritative-nunit-reporting.yaml
```
