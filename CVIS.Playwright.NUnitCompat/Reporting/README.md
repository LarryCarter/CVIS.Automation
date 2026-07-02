# Playwright NUnitCompat Reporting

# Purpose

This folder contains lifecycle reporting support used by the Playwright/NUnit compatibility layer.

# Responsibilities

- Support diagnostic lifecycle output.
- Keep browser lifecycle reporting separate from authoritative test execution reporting.
- Direct developers to the authoritative TRX/NUnit XML reporting path for full counts.

# When to use

Use this folder when diagnosing Playwright-specific lifecycle behavior.

# When NOT to use

Do not treat lifecycle report output as the authoritative test total.

# Architecture

Authoritative report inputs:

```text
TestResults\TRX
TestResults\NUnitXml
```

Authoritative report outputs:

```text
TestResults\CPN\cpn-report.html
TestResults\CPN\cpn-report.json
TestResults\CPN\cpn-report-all-tests.html
TestResults\CPN\cpn-report-all-tests.json
TestResults\CPN\cpn-report-summary.txt
TestResults\CPN\Tests\*.json
```

Diagnostic lifecycle report:

```text
TestResults\CPN\cpn-lifecycle-report.html
```

HyperExecute parses NUnit XML from:

```text
TestResults\NUnitXml
```

# Examples

HyperExecute entry point:

```text
hyperexecute-cvis-authoritative-nunit.yaml
```

Local full run:

```powershell
.\scripts\run-cvis-authoritative-report-local.ps1 -Configuration Debug -MinimumTotal 250
```

# Common mistakes

- Uploading only lifecycle output and thinking all NUnit tests were counted.
- Comparing Visual Studio test count to lifecycle hook count.
- Pointing HyperExecute at CPN HTML instead of NUnit XML.
- Forgetting to upload `TestResults\CPN` as an artifact after the parser reads `TestResults\NUnitXml`.

# Related folders

- `CVIS.Playwright.Reporting`
- `CVIS.Playwright.Reporting.Tool`
- `scripts`
