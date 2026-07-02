# CVIS.Playwright.Reporting

# Purpose

This project contains the report models and builders used to create CVIS authoritative test reports.

# Responsibilities

- Read TRX result files.
- Read NUnit XML result files.
- Deduplicate test entries from TRX and NUnit XML.
- Write the CVIS report package under `TestResults\CPN`.

# When to use

Use this project when changing the report model, report builder, report HTML, report JSON, or result-file parsing behavior.

# When NOT to use

Do not use this project as the test runner. Test execution belongs to `dotnet test` and the local/pipeline scripts.

# Architecture

Report inputs:

```text
TestResults\TRX\**\*.trx
TestResults\NUnitXml\**\*.xml
```

Report outputs:

```text
TestResults\CPN\cpn-report.html
TestResults\CPN\cpn-report.json
TestResults\CPN\cpn-report-all-tests.html
TestResults\CPN\cpn-report-all-tests.json
TestResults\CPN\cpn-report-summary.txt
TestResults\CPN\Tests\*.json
```

The report summary source is `TRX+NUnitXml`.

# Examples

The reporting tool calls this project after tests run:

```powershell
dotnet run --project .\CVIS.Playwright.Reporting.Tool\CVIS.Playwright.Reporting.Tool.csproj -- `
  --trx-root .\TestResults\TRX `
  --nunit-xml-root .\TestResults\NUnitXml `
  --output-root .\TestResults\CPN `
  --framework-name "CVIS Authoritative Test Run" `
  --minimum-total 250
```

# Common mistakes

- Treating lifecycle diagnostics as the full report.
- Generating CPN output without TRX and NUnit XML input.
- Adding new report output formats without updating the pipeline post checks.

# Related folders

- `CVIS.Playwright.Reporting.Tool`
- `CVIS.FunctionalTesting/Reporting`
- `CVIS.Playwright.NUnitCompat/Reporting`
- `scripts`
