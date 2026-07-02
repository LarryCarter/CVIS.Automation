# CVIS.Playwright.Reporting.Tool

# Purpose

This project is the command-line entry point that creates the authoritative CVIS report package after test execution.

# Responsibilities

- Accept TRX, NUnit XML, output root, framework name, and minimum total arguments.
- Call `CVIS.Playwright.Reporting` to build the report.
- Fail the run when the authoritative result count is below the configured guardrail.

# When to use

Use this tool after `dotnet test` has written TRX and NUnit XML files.

# When NOT to use

Do not use this tool before test execution. It does not run tests by itself.

# Architecture

Required inputs:

```text
--trx-root
--nunit-xml-root
--output-root
```

Optional inputs:

```text
--framework-name
--minimum-total
```

Output files:

```text
TestResults\CPN\cpn-report.html
TestResults\CPN\cpn-report.json
TestResults\CPN\cpn-report-all-tests.html
TestResults\CPN\cpn-report-all-tests.json
TestResults\CPN\cpn-report-summary.txt
TestResults\CPN\Tests\*.json
```

# Examples

```powershell
dotnet run --project .\CVIS.Playwright.Reporting.Tool\CVIS.Playwright.Reporting.Tool.csproj -- `
  --trx-root .\TestResults\TRX `
  --nunit-xml-root .\TestResults\NUnitXml `
  --output-root .\TestResults\CPN `
  --framework-name "CVIS Authoritative Test Run" `
  --minimum-total 250
```

# Pipeline

The pipeline calls this tool through:

```powershell
.\scripts\run-cvis-authoritative-report-local.ps1
```

The pipeline should then verify the generated files and upload:

```text
TestResults\TRX
TestResults\NUnitXml
TestResults\CPN
```

# Common mistakes

- Pointing `--nunit-xml-root` at TRX output.
- Pointing the pipeline parser at CPN HTML instead of NUnit XML.
- Forgetting to update pipeline post checks when this tool writes a new output format.

# Related folders

- `CVIS.Playwright.Reporting`
- `scripts`
- `hyperexecute-cvis-authoritative-nunit.yaml`
