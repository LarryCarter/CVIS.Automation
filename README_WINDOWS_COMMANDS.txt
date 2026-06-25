# Three Lane NUnit HyperExecute Architecture

This RDEL package applies the architecture:

1. Plain NUnit functional lane
2. Optional Playwright browser lane
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

The CPN HTML report is generated from the same source plus TRX.
