# PolicyDrift Database Smoke Tests

## Connection string locations

The database smoke tests use this config path:

```json
{
  "Projects": {
    "PolicyDrift": {
      "Database": {
        "ConnectionString": "Server=THOUSANDSUNNY;Database=EPV_REPORTING;Trusted_Connection=True;TrustServerCertificate=True;"
      }
    }
  }
}
```

This patch also writes the same value to:

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=THOUSANDSUNNY;Database=EPV_REPORTING;Trusted_Connection=True;TrustServerCertificate=True;"
  }
}
```

## Why database tests are disabled by default

The smoke tests physically open a SQL Server connection. If the test machine, local workstation, or HyperExecute runner cannot resolve or reach:

```text
THOUSANDSUNNY
```

the test will fail with:

```text
Named Pipes Provider, error: 40 - Could not open a connection to SQL Server
```

So the safe default is:

```json
{
  "TestSettings": {
    "RunDatabaseTests": false
  }
}
```

## How to intentionally run DB smoke tests

Only enable this when the machine running the test can reach SQL Server:

```json
{
  "TestSettings": {
    "RunDatabaseTests": true
  }
}
```

Then run:

```powershell
dotnet test .\CVIS.Automation.Tests\CVIS.Automation.Tests.csproj --filter TestCategory=DatabaseRegression
```
