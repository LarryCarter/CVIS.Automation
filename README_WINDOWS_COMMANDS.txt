# CVIS Playwright NUnitCompat Test Project

This is a Contollo RDEL plugin-compatible update package.

## Purpose

This creates a separate NUnit test project for the CVIS replacement of `Microsoft.Playwright.NUnit`.

## New project

```text
CVIS.Playwright.NUnitCompat.Tests
```

## Why separate project

The compatibility layer should be tested like its own library. These tests should not live inside:

```text
CVIS.Automation.Tests
```

because that project is for functional automation such as PolicyDrift.

## What this package does

- Creates `CVIS.Playwright.NUnitCompat.Tests`
- References `CVIS.Playwright.NUnitCompat`
- Adds NUnit-based unit/compatibility tests
- Removes previously embedded compatibility tests under:
  `CVIS.Automation.Tests\Shared\PlaywrightCompatTests`
- Adds the new test project to the solution when a `.sln` file exists

## Test coverage added

- Settings provider:
  - default browser
  - supported browsers
  - invalid browser rejection
  - `HEADED`
  - `PWDEBUG`
  - `EXPECT_TIMEOUT`
  - `SLOW_MO`
  - `TEST_ID_ATTRIBUTE`
- Base class hierarchy:
  - `CVISPlaywrightTest`
  - `CVISBrowserTest`
  - `CVISContextTest`
  - `CVISPageTest`
  - `CVISApiTest`
- Runtime setup:
  - Playwright runtime initializes
  - browser name resolves
  - browser type resolves
- API request support:
  - default `ApiContext`
  - `NewApiRequestContextAsync`
  - `NewApiContextAsync`
- Browser/context contract:
  - context defaults
  - browser launch/connect extension points

## Commands run by plugin

```powershell
python .\add_cvis_playwright_nunitcompat_test_project.py
dotnet restore .\CVIS.Playwright.NUnitCompat\CVIS.Playwright.NUnitCompat.csproj
dotnet build .\CVIS.Playwright.NUnitCompat\CVIS.Playwright.NUnitCompat.csproj
dotnet restore .\CVIS.Playwright.NUnitCompat.Tests\CVIS.Playwright.NUnitCompat.Tests.csproj
dotnet build .\CVIS.Playwright.NUnitCompat.Tests\CVIS.Playwright.NUnitCompat.Tests.csproj
dotnet test .\CVIS.Playwright.NUnitCompat.Tests\CVIS.Playwright.NUnitCompat.Tests.csproj --filter TestCategory=PlaywrightCompatUnit
```

## Important

This package does not replace PolicyDrift tests and does not remove `Microsoft.Playwright.NUnit` from `CVIS.Automation.Tests`.
