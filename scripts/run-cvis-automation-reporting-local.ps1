param([string]$Configuration = "Debug")

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$TestResults = Join-Path $Root "TestResults"
$CpnResults = Join-Path $TestResults "CPN"
$NUnitResults = Join-Path $TestResults "NUnit"
$NUnitXmlResults = Join-Path $TestResults "NUnitXml"

if (Test-Path $TestResults) {
    Remove-Item $TestResults -Recurse -Force
}

New-Item -ItemType Directory -Force -Path $CpnResults | Out-Null
New-Item -ItemType Directory -Force -Path $NUnitResults | Out-Null
New-Item -ItemType Directory -Force -Path $NUnitXmlResults | Out-Null

$env:CPN_REPORT_ENABLED = "true"
$env:CPN_REPORT_ROOT = $CpnResults

dotnet test "$Root\CVIS.Automation.Tests\CVIS.Automation.Tests.csproj" `
    --configuration $Configuration `
    --logger "trx;LogFileName=cvis-automation-tests.trx" `
    --results-directory "$NUnitResults" `
    -- NUnit.TestOutputXml="$NUnitXmlResults"

Write-Host ""
Write-Host "Expected output:"
Write-Host "  $NUnitXmlResults"
Write-Host "  $NUnitResults"
Write-Host "  $CpnResults"
Write-Host ""
Write-Host "Note: CPN report files only include tests that inherit from CPN base classes."
