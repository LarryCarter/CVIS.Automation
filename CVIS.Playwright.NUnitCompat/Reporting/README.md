# Playwright NUnitCompat Reporting

# Purpose

This folder contains lifecycle reporting support used by the Playwright/NUnit compatibility layer.

# Responsibilities

- Support diagnostic lifecycle output.
- Keep browser lifecycle reporting separate from authoritative test execution reporting.

# When to use

Use this folder when diagnosing Playwright-specific lifecycle behavior.

# When NOT to use

Do not treat lifecycle report output as the authoritative test total.

# Architecture

Authoritative report:

```text
TestResults\CPN\cpn-report.html
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
.\scripts\run-cvis-authoritative-report-local.ps1
```

# Common mistakes

- Uploading only lifecycle output and thinking all NUnit tests were counted.
- Comparing Visual Studio test count to lifecycle hook count.

# Related folders

- `CVIS.Playwright.Reporting`
- `CVIS.Playwright.Reporting.Tool`
- `scripts`
