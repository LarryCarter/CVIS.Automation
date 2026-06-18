# CVIS Playwright NUnitCompat Feature Layer

This is a Contollo RDEL plugin-compatible update package.

## Purpose

This package creates an isolated CVIS compatibility layer before replacing `Microsoft.Playwright.NUnit`.

It does not modify PolicyDrift tests.

## New class library

```text
CVIS.Playwright.NUnitCompat
```

## Features added

- `CVISWorkerAwareTest`
- `CVISPlaywrightSettingsProvider`
- `CVISPlaywrightSettings`
- `CVISPlaywrightTest`
- `CVISBrowserService`
- `CVISBrowserTest`
- `CVISContextTest`
- `CVISPageTest`
- `CVISApiTest`

## Feature coverage

This recreates the major useful features of `Microsoft.Playwright.NUnit`:

- Playwright runtime setup
- Browser name selection from `BROWSER`
- `HEADED` / `PWDEBUG` support
- expect timeout support from `EXPECT_TIMEOUT`
- slow motion support from `SLOW_MO`
- test-id selector setup using `data-testid`
- `Expect(...)` helper methods
- browser service
- browser launch/connect extension points
- browser context tracking and teardown
- default context options
- page setup
- API request context support

## Tests added

```text
CVIS.Automation.Tests\Shared\PlaywrightCompatTests
```

The tests verify:

- settings provider behavior
- Playwright runtime setup
- APIRequestContext loopback call through Microsoft.Playwright
- class hierarchy compatibility

## Commands run by plugin

```powershell
python .\add_cvis_playwright_nunitcompat_features.py
dotnet restore .\CVIS.Playwright.NUnitCompat\CVIS.Playwright.NUnitCompat.csproj
dotnet build .\CVIS.Playwright.NUnitCompat\CVIS.Playwright.NUnitCompat.csproj
dotnet restore .\CVIS.Automation.Tests\CVIS.Automation.Tests.csproj
dotnet build .\CVIS.Automation.Tests\CVIS.Automation.Tests.csproj
dotnet test .\CVIS.Automation.Tests\CVIS.Automation.Tests.csproj --filter TestCategory=PlaywrightCompatibility
```

## Important

This package intentionally keeps the real `Microsoft.Playwright.NUnit` package in place for now. Replacement should only happen after this compatibility layer builds and tests pass.
