# CVIS Playwright NUnit Compatibility Layer

This is a Contollo RDEL plugin-compatible update package.

## Purpose

This package creates a separate class library that recreates the useful features of `Microsoft.Playwright.NUnit` under CVIS-owned classes.

This does **not** replace PolicyDrift tests yet.

## New class library

```text
CVIS.Playwright.NUnitCompat
```

## New CVIS compatibility classes

```text
CVISPlaywrightSettingsProvider
CVISPlaywrightTest
CVISBrowserService
CVISBrowserTest
CVISContextTest
CVISPageTest
CVISApiTest
```

## New compatibility tests

```text
CVIS.Automation.Tests\Shared\PlaywrightCompatTests
```

## Feature coverage

- NUnit `[SetUp]` lifecycle integration.
- Shared `IPlaywright` runtime.
- `BrowserName` resolution from environment.
- `BrowserType` resolution.
- Test-id selector attribute support.
- `Expect(...)` assertion helpers.
- Default expect timeout support.
- Browser launch support.
- Browser context creation and tracking.
- Context cleanup on successful tests.
- Context defaults: `Locale = en-US`, `ColorScheme = Light`.
- Page creation.
- API request context creation.
- Real Playwright API request test through a local loopback HTTP probe.

## Explicitly not changed yet

- PolicyDrift tests are not replaced.
- `Microsoft.Playwright.NUnit` is not removed from the main test project yet.
- This package only builds the CVIS compatibility layer and validates it.

## Commands run by the plugin

```powershell
python .\add_cvis_playwright_nunit_compat_layer.py
dotnet restore .\CVIS.Playwright.NUnitCompat\CVIS.Playwright.NUnitCompat.csproj
dotnet build .\CVIS.Playwright.NUnitCompat\CVIS.Playwright.NUnitCompat.csproj
dotnet restore .\CVIS.Automation.Tests\CVIS.Automation.Tests.csproj
dotnet build .\CVIS.Automation.Tests\CVIS.Automation.Tests.csproj
dotnet test .\CVIS.Automation.Tests\CVIS.Automation.Tests.csproj --filter TestCategory=CVISPlaywrightCompat
```
