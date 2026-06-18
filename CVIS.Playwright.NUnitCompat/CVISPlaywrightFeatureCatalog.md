# CVIS Playwright NUnit Compatibility Layer Feature Catalog

This project recreates the practical features of `Microsoft.Playwright.NUnit` under CVIS-owned base classes.

| Microsoft.Playwright.NUnit | CVIS replacement |
|---|---|
| `PlaywrightTest` | `CVISPlaywrightTest` |
| `BrowserTest` | `CVISBrowserTest` |
| `ContextTest` | `CVISContextTest` |
| `PageTest` | `CVISPageTest` |
| API support | `CVISApiTest` |
| Settings provider | `CVISPlaywrightSettingsProvider` |
| Browser service | `CVISBrowserService` |

Recreated behavior includes NUnit setup lifecycle, shared Playwright runtime, browser selection from environment, browser type resolution, data-testid selector configuration, Expect helpers, default expect timeout support, browser launch, browser context tracking, context cleanup, default context options, page creation, and API request context creation.
