# CVIS Fix Loopback HTTP Server

This is a Contollo RDEL plugin-compatible package.

## Problem

`CVIS.Automation.Tests\Shared\PlaywrightCompatTests\LoopbackHttpServer.cs` had malformed C# string constants in the HTTP response header section.

The build errors included:

```text
CS1010 Newline in constant
CS1002 ; expected
CS0103 Content does not exist in the current context
```

## Fix

This package rewrites only:

```text
CVIS.Automation.Tests\Shared\PlaywrightCompatTests\LoopbackHttpServer.cs
```

The replacement uses `StringBuilder` and explicit `\r\n` escape sequences.

## Commands

```powershell
python .\fix_loopback_http_server.py
dotnet restore .\CVIS.Automation.Tests\CVIS.Automation.Tests.csproj
dotnet build .\CVIS.Automation.Tests\CVIS.Automation.Tests.csproj
dotnet test .\CVIS.Automation.Tests\CVIS.Automation.Tests.csproj --filter TestCategory=PlaywrightCompatibility
```
