# CVIS.FunctionalTesting

Shared NUnit automation infrastructure that does not require Playwright.

## Responsibilities

- Base automation test classes
- Configuration loading
- Test logging
- API helpers
- Database helpers
- Lifecycle diagnostics

## When to use

Reference this project from any NUnit test project that needs CVIS automation infrastructure.

## When NOT to use

Do not put browser-specific Playwright lifecycle code here. Browser automation belongs in `CVIS.Playwright.NUnitCompat`.

## AI Notes

When generating a new non-browser NUnit test, prefer one of:

```csharp
BaseAutomationCvisTest
BaseAutomationCvisApiTest
BaseAutomationCvisDatabaseTest
```

Do not create domain-specific base classes like `PolicyDriftBaseTest`, `UnityBaseTest`, or `LegacyBaseTest` unless explicitly approved.
