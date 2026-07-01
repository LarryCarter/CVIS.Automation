# Helpers

# Purpose

This folder contains helper classes for non-browser functional tests.

# Responsibilities

- Provide reusable helpers that do not require Playwright.
- Keep HTTP/API helper logic outside individual test classes.
- Support the official API base class.

# When to use

Use helpers from this folder when a non-browser test needs reusable infrastructure such as API calls.

# When NOT to use

Do not add Playwright browser, context, or page helpers here. Put browser-specific helpers in the Playwright project.

# Architecture

`ApiClient` is intended to be used through `BaseAutomationCvisApiTest`, which creates and disposes it during the standard CVIS lifecycle.

# Examples

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

# Common mistakes

- Manually newing up `ApiClient` in every test when `BaseAutomationCvisApiTest` should be used.
- Adding browser helpers to this non-browser project.
- Hardcoding URLs instead of using `FunctionalTestConfig`.

# Related folders

- `CVIS.FunctionalTesting/Base`
- `CVIS.FunctionalTesting/Config`
