# Configuration

This folder owns shared test configuration.

## Main file

```text
appsettings.test.json
```

## Rules

- Configuration can enable or configure behavior.
- Configuration should not hide test discovery.
- Avoid silent skips.
- Database connection strings should live under the shared CVIS config path.
- Secrets should come from environment variables or secure CI variables when possible.

## AI Notes

When generating tests, do not hardcode machine-specific paths, URLs, or connection strings. Read them through `FunctionalTestConfig`.
