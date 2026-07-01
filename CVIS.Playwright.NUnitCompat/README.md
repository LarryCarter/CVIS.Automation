# CVIS.Playwright.NUnitCompat

# Purpose

This project contains CVIS Playwright/NUnit compatibility and browser automation infrastructure.

# Responsibilities

- Provide Playwright-compatible NUnit support.
- Provide official CVIS browser base classes under `Base`.
- Keep browser automation separate from non-browser functional infrastructure.
- Support lifecycle and report integration for browser tests.

# When to use

Use this project when a test needs browser automation or Playwright primitives.

Use one of these CVIS automation bases for new browser tests:

| Need | Base class |
|---|---|
| Browser-level setup, no automatic fresh page | `BaseAutomationCvisPlaywrightBrowserTest` |
| Fresh page/tab per test | `BaseAutomationCvisPlaywrightPageTabTest` |

# When NOT to use

Do not use this project for normal API, database, config, or console tests that do not need a browser.

Do not inherit old names for new CVIS automation tests:

```csharp
CVISPlaywrightTest
CVISPageTest
```

# Architecture

Browser automation extends the normal CVIS lifecycle through hook overrides. Specialized browser base classes should not declare their own NUnit lifecycle attributes.

# Examples

```csharp
public sealed class LoginPageTests : BaseAutomationCvisPlaywrightPageTabTest
{
    [Test]
    public async Task LoginPage_ShouldOpen()
    {
        await Page.GotoAsync(Config.BaseUrl);
        Assert.That(Page.Url, Is.Not.Empty);
    }
}
```

# Common mistakes

- Using browser base classes for non-browser tests.
- Using the root compatibility-layer classes when a CVIS automation base class is intended.
- Confusing lifecycle diagnostics with authoritative NUnit results.

# Related folders

- `CVIS.Playwright.NUnitCompat/Base`
- `CVIS.Playwright.NUnitCompat/Reporting`
- `CVIS.FunctionalTesting`
- `CVIS.Playwright.Reporting`
- `CVIS.Playwright.Reporting.Tool`

# Reporting

This is the report that should match real NUnit execution and HyperExecute results:

```text
TestResults\CPN\cpn-report.html
```

Lifecycle report is diagnostic only:

```text
TestResults\CPN\cpn-lifecycle-report.html
```

This only reflects tests that went through lifecycle hooks. Do not use it as the test total.

# Local full run

```powershell
.\scripts\run-cvis-authoritative-report-local.ps1
```

# HyperExecute

Use:

```text
hyperexecute-cvis-authoritative-nunit.yaml
```

HyperExecute parses:

```text
TestResults\NUnitXml
```

The CVIS HTML report is uploaded as an artifact from:

```text
TestResults\CPN
```
