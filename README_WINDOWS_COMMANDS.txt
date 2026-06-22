# CVIS Organize Shared CPN Projects

This is a Contollo RDEL plugin-compatible package.

## Goal

Separate responsibilities cleanly:

```text
CVIS.Playwright.NUnitCompat
CVIS.Playwright.NUnitCompat.Tests
CVIS.Playwright.Automation.Shared
CVIS.Automation.Tests
```

## Moves to CVIS.Playwright.Automation.Shared

From:

```text
CVIS.Automation.Tests\Shared
```

To:

```text
CVIS.Playwright.Automation.Shared
```

Folders moved:

```text
Console
Database
Helpers
Reporting
```

Namespaces change from:

```csharp
CVIS.Automation.Tests.Shared.*
```

to:

```csharp
CVIS.Playwright.Automation.Shared.*
```

## Removed from CVIS.Automation.Tests

```text
Shared\PlaywrightCompatTests
```

Those tests belong in:

```text
CVIS.Playwright.NUnitCompat.Tests
```

## Stays in CVIS.Automation.Tests for now

If present:

```text
Shared\Api
Shared\Playwright
```

Those are transitional until PolicyDrift is migrated to CPN.

## Commands

```powershell
python .\organize_shared_cpn_projects.py
dotnet restore .\CVIS.Playwright.Automation.Shared\CVIS.Playwright.Automation.Shared.csproj
dotnet build .\CVIS.Playwright.Automation.Shared\CVIS.Playwright.Automation.Shared.csproj
dotnet restore .\CVIS.Playwright.NUnitCompat\CVIS.Playwright.NUnitCompat.csproj
dotnet build .\CVIS.Playwright.NUnitCompat\CVIS.Playwright.NUnitCompat.csproj
dotnet restore .\CVIS.Playwright.NUnitCompat.Tests\CVIS.Playwright.NUnitCompat.Tests.csproj
dotnet build .\CVIS.Playwright.NUnitCompat.Tests\CVIS.Playwright.NUnitCompat.Tests.csproj
dotnet test .\CVIS.Playwright.NUnitCompat.Tests\CVIS.Playwright.NUnitCompat.Tests.csproj --filter TestCategory=PlaywrightCompatUnit
dotnet restore .\CVIS.Automation.Tests\CVIS.Automation.Tests.csproj
dotnet build .\CVIS.Automation.Tests\CVIS.Automation.Tests.csproj
```
