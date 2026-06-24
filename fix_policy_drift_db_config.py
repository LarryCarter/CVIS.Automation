r"""
CVIS RDEL Update Script
Package: Fix PolicyDrift DB Config

Purpose:
    Fix database smoke-test configuration.

    The PolicyDrift DB smoke tests read:
        Projects:PolicyDrift:Database:ConnectionString

    They do not read only:
        ConnectionStrings:DefaultConnection

    This patch writes both locations and disables database smoke tests by default
    so CI/HyperExecute/local runs do not fail unless the SQL Server is reachable.

    To run DB smoke tests intentionally, set:
        TestSettings:RunDatabaseTests = true
"""

from pathlib import Path
import json

ROOT = Path.cwd()
APPSETTINGS = ROOT / "CVIS.Automation.Tests" / "appsettings.test.json"

DB_CONNECTION = (
    "Server=THOUSANDSUNNY;"
    "Database=EPV_REPORTING;"
    "Trusted_Connection=True;"
    "TrustServerCertificate=True;"
)

def main() -> None:
    if APPSETTINGS.exists():
        raw = APPSETTINGS.read_text(encoding="utf-8-sig")
        data = json.loads(raw) if raw.strip() else {}
    else:
        data = {}

    data.setdefault("ConnectionStrings", {})
    data["ConnectionStrings"]["DefaultConnection"] = DB_CONNECTION

    data.setdefault("Projects", {})
    data["Projects"].setdefault("PolicyDrift", {})
    data["Projects"]["PolicyDrift"].setdefault("Database", {})
    data["Projects"]["PolicyDrift"]["Database"]["ConnectionString"] = DB_CONNECTION

    data.setdefault("TestSettings", {})
    data["TestSettings"]["RunDatabaseTests"] = False

    APPSETTINGS.parent.mkdir(parents=True, exist_ok=True)
    APPSETTINGS.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    readme = ROOT / "README_POLICYDRIFT_DB_TESTS.md"
    readme.write_text(
        """# PolicyDrift Database Smoke Tests

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
dotnet test .\\CVIS.Automation.Tests\\CVIS.Automation.Tests.csproj --filter TestCategory=DatabaseRegression
```
""",
        encoding="utf-8",
    )

    print("Updated PolicyDrift database config.")
    print("RunDatabaseTests is false by default.")
    print("Connection string was written to both DefaultConnection and Projects.PolicyDrift.Database.ConnectionString.")

if __name__ == "__main__":
    main()
