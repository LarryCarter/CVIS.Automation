# CVIS.Playwright.NUnitCompat

This project contains the optional Playwright browser lane for NUnit tests.

## When to use

Use this project only when a test needs browser automation.

## Base classes

| Need | Base class |
|---|---|
| Playwright + browser, manual context/page handling | `BaseAutomationCvisPlaywrightBrowserTest` |
| Playwright + browser + fresh page/tab per test | `BaseAutomationCvisPlaywrightPageTabTest` |

## Recommended default for UI tests

Most UI tests should inherit:

```csharp
BaseAutomationCvisPlaywrightPageTabTest
```

This gives each test a fresh browser page/tab.

## Do not use Playwright for everything

API, database, PolicyDrift, Unity, LegacySustainment, config, and logic tests should not inherit Playwright classes unless they need a browser.

## Legacy compatibility

Older compatibility classes may still exist:

```csharp
CVISPlaywrightTest
CVISBrowserTest
CVISContextTest
CVISPageTest
```

New developer-facing tests should prefer the clearer `BaseAutomationCvis...` names.
