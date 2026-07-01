# CVIS.FunctionalTesting

# Purpose

This project contains the shared NUnit automation infrastructure that does not require Playwright.

# Responsibilities

- Base automation test classes.
- Configuration loading.
- Test logging.
- API helpers.
- Database helpers.
- Lifecycle diagnostics.

# When to use

Reference this project from any NUnit test project that needs CVIS automation infrastructure without browser automation.

Use one of these base classes:

| Need | Base class |
|---|---|
| Normal NUnit functional test, no browser | `BaseAutomationCvisTest` |
| API test | `BaseAutomationCvisApiTest` |
| SQL/database test | `BaseAutomationCvisDatabaseTest` |

# When NOT to use

Do not put browser-specific Playwright lifecycle code here. Browser automation belongs in `CVIS.Playwright.NUnitCompat`.

Do not create domain-specific base classes here.

# Architecture

`BaseAutomationCvisTest` owns the NUnit lifecycle attributes for the non-browser functional base hierarchy.

Specialized base classes override lifecycle hooks instead of declaring new NUnit lifecycle attributes:

```csharp
OnFixtureSetUpAsync
OnTestSetUpAsync
OnTestTearDownAsync
OnFixtureTearDownAsync
```

# Examples

```csharp
public sealed class ConfigSmokeTests : BaseAutomationCvisTest
{
    [Test]
    public void Config_ShouldLoad()
    {
        Assert.That(Config, Is.Not.Null);
    }
}
```

# Common mistakes

- Adding Playwright references to this project.
- Creating `PolicyDriftBaseTest`, `UnityBaseTest`, or `LegacySustainmentBaseTest`.
- Putting NUnit `[SetUp]` or `[TearDown]` attributes in specialized base classes.
- Using `BaseAutomationCvisTest` for API tests that should use `BaseAutomationCvisApiTest`.

# Related folders

- `CVIS.FunctionalTesting/Base` — canonical non-browser base classes.
- `CVIS.FunctionalTesting/Config` — config loading.
- `CVIS.FunctionalTesting/Helpers` — helper classes like `ApiClient`.
- `CVIS.FunctionalTesting/Reporting` — lifecycle diagnostics.
- `CVIS.Playwright.NUnitCompat` — browser automation support.
