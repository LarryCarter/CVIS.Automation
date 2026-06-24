# CPN Migration

## Removed / blocked packages

These packages should not be used by CVIS after the CPN migration:

```text
Microsoft.Playwright.NUnit
System.Text.Json explicit PackageReference
xUnit packages
```

## Kept packages

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

## CPN replacement classes

```text
Microsoft.Playwright.NUnit.PlaywrightTest -> CVISPlaywrightTest
Microsoft.Playwright.NUnit.BrowserTest    -> CVISBrowserTest
Microsoft.Playwright.NUnit.ContextTest    -> CVISContextTest
Microsoft.Playwright.NUnit.PageTest       -> CVISPageTest
API helper usage                           -> CVISApiTest
```

## DB configuration

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=THOUSANDSUNNY;Database=EPV_REPORTING;Trusted_Connection=True;TrustServerCertificate=True;"
  }
}
```
