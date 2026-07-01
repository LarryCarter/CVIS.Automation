# Base Automation Test Classes

These are the official base classes developers should choose from.

## BaseAutomationCvisTest

Use for normal NUnit automation tests that need:

- CVIS configuration
- logging
- lifecycle diagnostics

Do not use this if the test specifically needs an API client, database connection helpers, or browser automation.

## BaseAutomationCvisApiTest

Use for API tests.

Adds:

- `ApiClient`
- API configuration from `appsettings.test.json`
- automatic API client setup/disposal

## BaseAutomationCvisDatabaseTest

Use for SQL/database tests.

Adds:

- `DatabaseConnectionString`
- `OpenDatabaseConnectionAsync`
- `AssertDatabaseConnectionCanOpenAsync`
- connection cleanup

## Browser tests

Browser tests live in `CVIS.Playwright.NUnitCompat\Base`.

Use:

```csharp
BaseAutomationCvisPlaywrightBrowserTest
BaseAutomationCvisPlaywrightPageTabTest
```

## Common mistakes

Do not create one base class per product/domain.

Bad:

```csharp
PolicyDriftBaseTest
UnityBaseTest
LegacySustainmentBaseTest
```

Good:

```csharp
BaseAutomationCvisApiTest
BaseAutomationCvisDatabaseTest
BaseAutomationCvisPlaywrightPageTabTest
```
