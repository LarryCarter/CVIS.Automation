# Authoritative HyperExecute / NUnit Reporting

## The important rule

The report that counts for HyperExecute must come from **NUnit XML**, not the CPN lifecycle report.

Visual Studio Test Explorer is showing NUnit-discovered tests. HyperExecute must be pointed at the same source:

```text
TestResults\NUnitXml
```

## Why the old CPN report only showed 2 tests

The old CPN lifecycle report only recorded tests inheriting from:

```csharp
CVISPlaywrightTest
CVISBrowserTest
CVISContextTest
CVISPageTest
CVISApiTest
```

Most of the existing PolicyDrift tests are NUnit tests. They count in Visual Studio and they count in NUnit XML, but they do not all pass through the CPN lifecycle.

So the correct reporting path is:

```text
dotnet test
  -> NUnit XML
       -> HyperExecute parsed report
       -> CPN full HTML report generated from NUnit XML
```

## Local authoritative run

Run this from the solution root:

```powershell
.\scripts\run-all-nunit-reporting-local.ps1
```

Expected outputs:

```text
TestResults\NUnitXml
TestResults\NUnit
TestResults\CPN\cpn-report.html
TestResults\CPN\cpn-report.json
TestResults\CPN\cpn-report-summary.txt
```

Open:

```text
TestResults\CPN\cpn-report.html
```

That report is generated from NUnit XML and should line up with the real NUnit test count.

## HyperExecute YAML

Use:

```text
hyperexecute-authoritative-nunit-reporting.yaml
```

The important section is:

```yaml
report: true
partialReports:
  type: nunit
  location: .\TestResults\NUnitXml
  frameworkName: nunit
```

That is what HyperExecute parses.

## CPN report is artifact only

The CPN HTML report is uploaded as an artifact:

```yaml
uploadArtefacts:
  - name: cvis-authoritative-test-output
    path:
      - .\TestResults\NUnitXml
      - .\TestResults\NUnit
      - .\TestResults\CPN
```

## Validation guard

The reporting script uses:

```text
--minimum-total 250
```

If the NUnit XML contains fewer than 250 tests, the report generation fails. This prevents submitting a HyperExecute run that only captured 2 or 11 tests.
