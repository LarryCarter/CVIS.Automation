# CPN Report README And Local Scripts

Adds:

```text
README_CPN_REPORT_OUTPUT.md
README_HYPEREXECUTE_CPN_REPORTING.md
scripts\run-cpn-reporting-local.ps1
scripts\run-cvis-automation-reporting-local.ps1
```

After applying, run:

```powershell
.\scripts\run-cpn-reporting-local.ps1
```

Expected output:

```text
TestResults\NUnitXml\*.xml
TestResults\NUnit\*.trx
TestResults\CPN\cpn-report.html
TestResults\CPN\cpn-report.json
TestResults\CPN\Tests\*.json
```
