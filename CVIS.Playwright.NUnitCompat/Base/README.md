# Playwright Base Automation Classes

# Purpose

This folder contains the official CVIS Playwright base classes for browser automation tests.

# Responsibilities

- Provide browser-level setup through `BaseAutomationCvisPlaywrightBrowserTest`.
- Provide fresh page/context per test through `BaseAutomationCvisPlaywrightPageTabTest`.
- Keep old class names only as temporary compatibility aliases.

# When to use

Use this folder when a test needs Playwright or browser automation.

| Test type | Use |
|---|---|
| Browser needed, no automatic page per test | `BaseAutomationCvisPlaywrightBrowserTest` |
| Browser plus fresh page/tab per test | `BaseAutomationCvisPlaywrightPageTabTest` |

# When NOT to use

Do not use this folder for API-only, database-only, config-only, or console-only tests.

Use non-browser bases from `CVIS.FunctionalTesting/Base` instead.

# Architecture

Clean final naming:

| Old | New |
|---|---|
| `CVISPlaywrightTest` | `BaseAutomationCvisPlaywrightBrowserTest` |
| `CVISPageTest` | `BaseAutomationCvisPlaywrightPageTabTest` |

The browser base classes inherit from `BaseAutomationCvisTest` and override lifecycle hooks.

# Examples

```csharp
public sealed class BrowserSmokeTests : BaseAutomationCvisPlaywrightBrowserTest
{
    [Test]
    public void Browser_ShouldLaunch()
    {
        Assert.That(Browser, Is.Not.Null);
    }
}
```

```csharp
public sealed class PageSmokeTests : BaseAutomationCvisPlaywrightPageTabTest
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

- Inheriting `CVISPageTest` in new code instead of `BaseAutomationCvisPlaywrightPageTabTest`.
- Adding `[SetUp]` or `[TearDown]` here instead of overriding lifecycle hooks.
- Using Playwright bases for tests that only need API or database access.

# Related folders

- `CVIS.FunctionalTesting/Base`
- `CVIS.Playwright.NUnitCompat/Reporting`
- `CVIS.Playwright.Reporting.Tool`
