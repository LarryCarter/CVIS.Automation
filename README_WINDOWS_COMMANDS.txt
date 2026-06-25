# Three Lane NUnit HyperExecute Architecture

This RDEL package applies the architecture:

1. Plain NUnit functional lane (BaseFunctionalTest)
2. Optional Playwright browser lane (CVISPlaywrightTest / CVISPageTest)
3. Authoritative reporting from TRX/NUnit XML

## After applying

Run:

```powershell
.\scripts\run-cvis-authoritative-report-local.ps1
```

Open:

```text
TestResults\CPN\cpn-report.html
```

## HyperExecute

Use:

```text
hyperexecute-cvis-authoritative-nunit.yaml
```

HyperExecute parses:

```text
TestResults\NUnitXml
```

The CPN HTML report is generated from the same TRX + NUnit XML source.
The cpn-lifecycle-report.* files come from CPN base class teardown hooks
and are for debugging only — do NOT use them for test totals.
