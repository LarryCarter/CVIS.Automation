# Playwright Base Automation Classes

# Purpose

This folder contains the official CVIS Playwright base classes for browser automation tests.

# Responsibilities

- Provide browser-level setup through `CvisAutomationPlaywrightBrowserTestBase`.
- Provide fresh page/context per test through `CvisAutomationPlaywrightPageTabTestBase`.
- Keep CVIS browser automation on the same lifecycle hook model as `CvisAutomationTestBase`.

# When to use

Use this folder when a test needs Playwright or browser automation.

| Test type | Use |
|---|---|
| Browser needed, no automatic page per test | `CvisAutomationPlaywrightBrowserTestBase` |
| Browser plus fresh page/tab per test | `CvisAutomationPlaywrightPageTabTestBase` |

# When NOT to use

Do not use this folder for API-only, database-only, config-only, or console-only tests.

Use non-browser bases from `CVIS.FunctionalTesting/Base` instead.

Use the current `CvisAutomationPlaywright*TestBase` names for new CVIS automation tests.

# Architecture

Final browser hierarchy:

```text
CvisAutomationTestBase
└── CvisAutomationPlaywrightBrowserTestBase
    └── CvisAutomationPlaywrightPageTabTestBase
```

The browser base classes inherit from `CvisAutomationTestBase` and override lifecycle hooks.

`CvisAutomationPlaywrightPageTabTestBase` imports `NUnit.Framework` because it uses `TestContext` while logging the fresh page setup.

# Examples

```csharp
public sealed class BrowserSmokeTests : CvisAutomationPlaywrightBrowserTestBase
{
    [Test]
    public void Browser_ShouldLaunch()
    {
        Assert.That(Browser, Is.Not.Null);
    }
}
```

```csharp
public sealed class PageSmokeTests : CvisAutomationPlaywrightPageTabTestBase
{
    [Test]
    public async Task Page_ShouldNavigate()
    {
        await Page.GotoAsync(Config.BaseUrl);
        Assert.That(Page.Url, Is.Not.Empty);
    }
}
```

# Common mistakes

- Inheriting the root Playwright compatibility classes when the CVIS automation base hierarchy is intended.
- Adding `[SetUp]` or `[TearDown]` here instead of overriding lifecycle hooks.
- Using Playwright bases for tests that only need API or database access.
- Using old base names after the rename to `CvisAutomationPlaywright*TestBase`.

# Related folders

- `CVIS.FunctionalTesting/Base`
- `CVIS.Playwright.NUnitCompat/Reporting`
- `CVIS.Playwright.Reporting.Tool`
