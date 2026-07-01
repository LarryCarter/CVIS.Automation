# CVIS.Automation.Tests

This project contains CVIS automation tests across products/domains such as PolicyDrift, Unity, and LegacySustainment.

## Base class selection

| Test type | Use |
|---|---|
| Normal NUnit automation | `BaseAutomationCvisTest` |
| API test | `BaseAutomationCvisApiTest` |
| Database test | `BaseAutomationCvisDatabaseTest` |
| Browser test | `BaseAutomationCvisPlaywrightPageTabTest` |

## Do not create domain base classes

Do not create:

```csharp
PolicyDriftBaseTest
UnityBaseTest
LegacySustainmentBaseTest
```

Those are domains. They may use API, database, browser, or normal automation bases depending on the specific test.

## Reporting

All tests are counted by NUnit/TRX output if they are discovered and executed by `dotnet test`.

A test does not need to inherit a CVIS base class to be counted by HyperExecute, but it should inherit the correct CVIS base if it needs shared CVIS services.
