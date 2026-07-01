# CVIS.Automation.Tests

# Purpose

This project contains CVIS automation tests across product/domain areas such as PolicyDrift, Unity, and LegacySustainment.

# Responsibilities

- Hold domain test cases.
- Use the correct CVIS base class by capability.
- Produce NUnit/TRX output for authoritative reporting.

# When to use

Use this project for test implementations against CVIS systems and workflows.

# When NOT to use

Do not put shared test infrastructure here. Shared infrastructure belongs in `CVIS.FunctionalTesting` or `CVIS.Playwright.NUnitCompat`.

# Architecture

Domains are folders or categories, not base classes.

| Need | Base class |
|---|---|
| Normal NUnit functional test, no browser | `BaseAutomationCvisTest` |
| API test | `BaseAutomationCvisApiTest` |
| SQL/database test | `BaseAutomationCvisDatabaseTest` |
| Browser-level Playwright test | `BaseAutomationCvisPlaywrightBrowserTest` |
| Fresh page/tab Playwright test | `BaseAutomationCvisPlaywrightPageTabTest` |

# Examples

PolicyDrift API test:

```csharp
public sealed class PolicyDriftApiTests : BaseAutomationCvisApiTest
{
    [Test]
    public async Task PolicyDriftEndpoint_ShouldRespond()
    {
        var response = await ApiClient.GetAsync("/policydrift/health");
        Assert.That(response.IsSuccessStatusCode, Is.True);
    }
}
```

# Common mistakes

- Creating `PolicyDriftBaseTest`.
- Using Playwright base classes for API, DB, or console tests.
- Assuming lifecycle report totals equal the full NUnit execution total.

# Related folders

- `CVIS.FunctionalTesting/Base`
- `CVIS.Playwright.NUnitCompat/Base`
- `scripts`
