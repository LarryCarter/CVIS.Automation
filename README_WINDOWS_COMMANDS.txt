# CPN Fix ResultAdapter Output

This is a focused Contollo RDEL plugin-compatible fix.

## Error fixed

```text
CS1061: TestContext.ResultAdapter does not contain a definition for Output
```

## Fix

Updates:

```text
CVIS.Playwright.NUnitCompat\Reporting\CPNReportManager.cs
```

Changes invalid result output access to:

```csharp
OutputLines = Array.Empty<string>()
```

Later, we can add a dedicated CPN output collector if we want captured output in the report.
