# CVIS.Automation

Shared NUnit and Playwright automation harness for CVIS projects.

# Purpose

This repository provides the shared automation infrastructure for CVIS functional, API, database, and browser tests.

# Responsibilities

- Provide canonical NUnit base classes for CVIS automation.
- Provide optional Playwright base classes only when browser automation is needed.
- Provide configuration loading, API helpers, database helpers, and lifecycle diagnostics.
- Generate authoritative reports from real NUnit/TRX execution output.
- Keep documentation clear enough that developers and AI assistants choose the correct base class.

# When to use

Use this repository when building CVIS automation tests for domains such as PolicyDrift, Unity, LegacySustainment, or future CVIS domains.

# When NOT to use

Do not use this repository as the application-under-test. It is an automation harness and test infrastructure repository.

Do not create domain-specific base classes such as:

```csharp
PolicyDriftBaseTest
UnityBaseTest
LegacySustainmentBaseTest
```

Domains are test areas. Base classes are capability layers.

# Architecture

## Canonical base class selection

| Need | Inherit from |
|---|---|
| Normal NUnit functional test, no browser | `BaseAutomationCvisTest` |
| API test | `BaseAutomationCvisApiTest` |
| SQL/database test | `BaseAutomationCvisDatabaseTest` |
| Playwright browser-level setup | `BaseAutomationCvisPlaywrightBrowserTest` |
| Playwright fresh page/tab per test | `BaseAutomationCvisPlaywrightPageTabTest` |

## Clean final naming

| Old | New | Meaning |
|---|---|---|
| `BaseFunctionalTest` | `BaseAutomationCvisTest` | normal NUnit functional test, no browser |
| `CVISPlaywrightTest` | `BaseAutomationCvisPlaywrightBrowserTest` | Playwright available, browser-level setup |
| `CVISPageTest` | `BaseAutomationCvisPlaywrightPageTabTest` | Playwright plus fresh page per test |

Legacy names may remain temporarily as obsolete compatibility aliases. New code must use the new names.

## Reporting

The report that should match real NUnit execution is:

```text
TestResults\CPN\cpn-report.html
```

Lifecycle report is diagnostic only:

```text
TestResults\CPN\cpn-lifecycle-report.html
```

The lifecycle report only reflects tests that went through lifecycle hooks. Do not use it as the test total.

# Examples

Normal functional test:

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

API test:

```csharp
public sealed class PlatformApiTests : BaseAutomationCvisApiTest
{
    [Test]
    public async Task Platforms_ShouldReturnSuccess()
    {
        var result = await ApiClient.GetJsonAsync<object[]>("/platforms");
        Assert.That(result, Is.Not.Null);
    }
}
```

Browser page test:

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

- Using Playwright base classes for tests that do not need a browser.
- Using lifecycle report totals as if they are full test totals.
- Creating domain-specific base classes.
- Adding NUnit lifecycle attributes to specialized base classes instead of overriding lifecycle hooks.

# Related folders

- `CVIS.FunctionalTesting` — non-browser NUnit automation infrastructure.
- `CVIS.Playwright.NUnitCompat` — Playwright/browser automation infrastructure.
- `CVIS.Playwright.Reporting` — report model and report generation support.
- `CVIS.Playwright.Reporting.Tool` — command-line report generation tool.
- `CVIS.Automation.Tests` — CVIS domain test implementations.
- `scripts` — local report and execution helpers.

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
