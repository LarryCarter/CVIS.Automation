# Playwright Base Automation Classes

These are the official Playwright base classes.

## BaseAutomationCvisPlaywrightBrowserTest

Use when the test needs Playwright and a browser, but wants to manually control browser context/page creation.

## BaseAutomationCvisPlaywrightPageTabTest

Use for most UI tests.

This provides:

- Playwright
- Browser
- Browser context
- Fresh page/tab per test

## Page/tab per test

A page is a browser tab.

Each test gets a fresh page/tab so cookies, session state, and UI state do not leak between tests.

## Do not use for

- API tests
- database tests
- PolicyDrift logic tests
- Unity logic tests
- LegacySustainment config tests

Use the non-browser base classes in `CVIS.FunctionalTesting\Base` instead.
