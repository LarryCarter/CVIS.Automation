# CVIS.Automation

Shared Playwright C# automation harness for CVIS projects.

## Projects

- PolicyDrift
- Unity
- LegacySustainment

## Setup

```powershell
dotnet build
pwsh .\CVIS.Automation.Tests\bin\Debug\net8.0\playwright.ps1 install
dotnet test
```

## Configuration

Edit `appsettings.test.json` to enable projects and set connection strings, API URLs, and console app paths.

## Running Specific Categories

```powershell
dotnet test --filter "TestCategory=PolicyDrift"
dotnet test --filter "TestCategory=DatabaseRegression"
dotnet test --filter "TestCategory=ApiRegression"
dotnet test --filter "TestCategory=ConsoleRegression"
dotnet test --filter "TestCategory=WorkflowRegression"
```
