# CVIS Automation / CPN Project Structure

## CVIS.Playwright.NUnitCompat

CPN runtime compatibility layer.

Contains the replacement classes for the useful parts of `Microsoft.Playwright.NUnit`:

- `CVISWorkerAwareTest`
- `CVISPlaywrightSettingsProvider`
- `CVISPlaywrightTest`
- `CVISBrowserService`
- `CVISBrowserTest`
- `CVISContextTest`
- `CVISPageTest`
- `CVISApiTest`

## CVIS.Playwright.NUnitCompat.Tests

CPN unit/compatibility tests.

This project validates CPN behavior separately from functional automation tests.

## CVIS.Playwright.Automation.Shared

Shared functional automation utilities.

This project owns shared non-CPN helpers:

- Console app execution helpers
- Database helpers
- Config/data loading helpers
- Regression report helpers

## CVIS.Automation.Tests

Functional regression test project.

This project should contain project-specific automation suites such as:

- PolicyDrift
- Unity
- LegacySustainment

It should not contain CPN compatibility tests.
