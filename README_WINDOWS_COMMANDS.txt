# CVIS Fix API Test Compatibility

This is a Contollo RDEL plugin-compatible package.

## Problem

The compatibility tests expect these members on `CVISApiTest`:

```csharp
ApiContext
NewApiRequestContextAsync(...)
```

The first feature layer only provided:

```csharp
NewApiContextAsync(...)
```

## Fix

This package rewrites:

```text
CVIS.Playwright.NUnitCompat\CVISApiTest.cs
```

It adds:

```csharp
public IAPIRequestContext ApiContext { get; private set; }
public Task<IAPIRequestContext> NewApiRequestContextAsync(...)
public Task<IAPIRequestContext> NewApiContextAsync(...)
```

## Commands

```powershell
python .\fix_cvis_api_test_compatibility.py
dotnet restore .\CVIS.Playwright.NUnitCompat\CVIS.Playwright.NUnitCompat.csproj
dotnet build .\CVIS.Playwright.NUnitCompat\CVIS.Playwright.NUnitCompat.csproj
dotnet restore .\CVIS.Automation.Tests\CVIS.Automation.Tests.csproj
dotnet build .\CVIS.Automation.Tests\CVIS.Automation.Tests.csproj
dotnet test .\CVIS.Automation.Tests\CVIS.Automation.Tests.csproj --filter TestCategory=PlaywrightCompatibility
```
