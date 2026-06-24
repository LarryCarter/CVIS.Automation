# Switch To CPN Remove Bad NuGets

This is a Contollo RDEL plugin-compatible package.

## Removes

```text
Microsoft.Playwright.NUnit
System.Text.Json explicit PackageReference
xUnit packages
```

## Keeps / uses

```text
Microsoft.Playwright
NUnit
NUnit3TestAdapter
NUnit.Analyzers
Microsoft.NET.Test.Sdk
FluentAssertions
coverlet.collector
Microsoft.Data.SqlClient
```

## Project updates

- Ensures `CVIS.Playwright.NUnitCompat` references `Microsoft.Playwright` and `NUnit`
- Ensures test projects reference CPN
- Ensures automation tests reference `CVIS.Playwright.Automation.Shared`
- Removes forbidden `PackageVersion` entries from `Directory.Packages.props`

## Code updates

Basic replacements:

```text
using Microsoft.Playwright.NUnit; -> using CVIS.Playwright.NUnitCompat;
PageTest       -> CVISPageTest
ContextTest    -> CVISContextTest
BrowserTest    -> CVISBrowserTest
PlaywrightTest -> CVISPlaywrightTest
```

## DB config update

Updates:

```text
CVIS.Automation.Tests\appsettings.test.json
```

to include:

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=THOUSANDSUNNY;Database=EPV_REPORTING;Trusted_Connection=True;TrustServerCertificate=True;"
  }
}
```

## Commands

```powershell
python .\switch_to_cpn_remove_bad_nugets.py
dotnet restore .\CVIS.Playwright.Automation.Shared\CVIS.Playwright.Automation.Shared.csproj
dotnet build .\CVIS.Playwright.Automation.Shared\CVIS.Playwright.Automation.Shared.csproj
dotnet restore .\CVIS.Playwright.NUnitCompat\CVIS.Playwright.NUnitCompat.csproj
dotnet build .\CVIS.Playwright.NUnitCompat\CVIS.Playwright.NUnitCompat.csproj
dotnet restore .\CVIS.Playwright.NUnitCompat.Tests\CVIS.Playwright.NUnitCompat.Tests.csproj
dotnet build .\CVIS.Playwright.NUnitCompat.Tests\CVIS.Playwright.NUnitCompat.Tests.csproj
dotnet test .\CVIS.Playwright.NUnitCompat.Tests\CVIS.Playwright.NUnitCompat.Tests.csproj --filter TestCategory=CPNReporting
dotnet restore .\CVIS.Automation.Tests\CVIS.Automation.Tests.csproj
dotnet build .\CVIS.Automation.Tests\CVIS.Automation.Tests.csproj
```
