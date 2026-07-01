# CVIS.Playwright.Reporting.Tool

Console tool that generates the authoritative CVIS report after `dotnet test`.

## Example

```powershell
dotnet run --project .\CVIS.Playwright.Reporting.Tool\CVIS.Playwright.Reporting.Tool.csproj -- `
  --trx-root .\TestResults\TRX `
  --nunit-xml-root .\TestResults\NUnitXml `
  --output-root .\TestResults\CPN `
  --framework-name "CVIS Authoritative Test Run" `
  --minimum-total 250
```

## Rules

- Run this after test execution.
- Use TRX + NUnit XML as input.
- Fail if the minimum expected total is not met.
