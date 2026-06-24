# CPN Full NUnit Report Bridge

Adds:

```text
scripts\merge-nunitxml-into-cpn-report.ps1
scripts\run-cpn-reporting-local.ps1
scripts\run-cvis-automation-reporting-local.ps1
README_CPN_FULL_REPORT_BRIDGE.md
```

After applying, run:

```powershell
.\scripts\run-cvis-automation-reporting-local.ps1
```

Expected full report:

```text
TestResults\CPN\cpn-report.html
TestResults\CPN\cpn-report.json
```

This report is generated from NUnit XML and includes all NUnit tests.
