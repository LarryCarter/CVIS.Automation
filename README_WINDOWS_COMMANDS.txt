# CVIS Fix NU1008 Central Package Versions

This is a Contollo RDEL plugin-compatible package.

## Problem

Projects using Central Package Version Management cannot define versions directly on `PackageReference` items.

Bad:

```xml
<PackageReference Include="FluentAssertions" Version="8.10.0" />
```

Correct:

```xml
<PackageReference Include="FluentAssertions" />
```

and in `Directory.Packages.props`:

```xml
<PackageVersion Include="FluentAssertions" Version="8.10.0" />
```

## What this package does

It scans all `.csproj` files under the solution and:

- removes `Version="..."` from `PackageReference`
- removes child `<Version>...</Version>` from `PackageReference`
- creates or updates `Directory.Packages.props`
- adds missing `PackageVersion` entries

## Packages covered

```text
FluentAssertions
Microsoft.Data.SqlClient
Microsoft.NET.Test.Sdk
Microsoft.Playwright
Microsoft.Playwright.NUnit
NUnit
NUnit3TestAdapter
NUnit.Analyzers
coverlet.collector
System.Text.Json
```

It also preserves any versions it discovers in existing project files.

## Commands

```powershell
python .\fix_nu1008_central_package_versions.py
dotnet restore .\CVIS.Playwright.Automation.Shared\CVIS.Playwright.Automation.Shared.csproj
dotnet build .\CVIS.Playwright.Automation.Shared\CVIS.Playwright.Automation.Shared.csproj
dotnet restore .\CVIS.Playwright.NUnitCompat\CVIS.Playwright.NUnitCompat.csproj
dotnet build .\CVIS.Playwright.NUnitCompat\CVIS.Playwright.NUnitCompat.csproj
dotnet restore .\CVIS.Playwright.NUnitCompat.Tests\CVIS.Playwright.NUnitCompat.Tests.csproj
dotnet build .\CVIS.Playwright.NUnitCompat.Tests\CVIS.Playwright.NUnitCompat.Tests.csproj
dotnet restore .\CVIS.Automation.Tests\CVIS.Automation.Tests.csproj
dotnet build .\CVIS.Automation.Tests\CVIS.Automation.Tests.csproj
```
