# Configuration

# Purpose

This folder contains configuration loading for CVIS functional tests.

# Responsibilities

- Load `appsettings.test.json`.
- Provide shared runtime settings such as base URLs, API URLs, database connection strings, environment names, and timeouts.
- Keep configuration behavior centralized for tests.

# When to use

Use this folder when a test needs CVIS automation configuration through `FunctionalTestConfig`.

# When NOT to use

Do not use configuration flags to hide broken tests or control test discovery. Use NUnit categories, filters, or `[Ignore]` for execution decisions.

# Architecture

`FunctionalTestConfig.Load()` searches for `appsettings.test.json` from the test output directory upward and returns default settings when the file is absent.

# Examples

```csharp
var config = FunctionalTestConfig.Load();
Assert.That(config.ApiBaseUrl, Is.Not.Empty);
```

# Common mistakes

- Treating config as a test runner.
- Putting secrets in committed config files.
- Assuming a missing config file should fail all tests.

# Related folders

- `CVIS.FunctionalTesting/Base`
- `CVIS.FunctionalTesting/Helpers`
