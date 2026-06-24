# Authoritative HyperExecute NUnit Reporting

After applying, run:

```powershell
.\scripts\run-all-nunit-reporting-local.ps1
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
