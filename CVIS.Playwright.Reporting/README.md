# CVIS.Playwright.Reporting

This project builds the authoritative CVIS HTML/JSON report.

## Source of truth

The report reads:

```text
TestResults\TRX
TestResults\NUnitXml
```

## Output

```text
TestResults\CPN\cpn-report.html
TestResults\CPN\cpn-report.json
TestResults\CPN\cpn-report-summary.txt
```

## Why this exists

Visual Studio, `dotnet test`, and HyperExecute rely on test runner output. Therefore the CVIS HTML report must be generated from the same runner output, not from custom teardown hooks.

## AI Notes

Do not change this project to read lifecycle logs as the authoritative source. Lifecycle logs are diagnostic only.
