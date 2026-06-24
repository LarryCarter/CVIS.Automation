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

dotnet test "$Root\CVIS.Playwright.NUnitCompat.Tests\CVIS.Playwright.NUnitCompat.Tests.csproj" `
    --configuration $Configuration `
    --logger "trx;LogFileName=cpn-tests.trx" `
    --results-directory "$NUnitResults" `
    -- NUnit.TestOutputXml="$NUnitXmlResults"

powershell -ExecutionPolicy Bypass -File "$Root\scripts\merge-nunitxml-into-cpn-report.ps1" `
    -NUnitXmlRoot "$NUnitXmlResults" `
    -CpnRoot "$CpnResults" `
    -FrameworkName "CVIS.Playwright.NUnitCompat"

Write-Host ""
Write-Host "Expected output:"
Write-Host "  $NUnitXmlResults"
Write-Host "  $NUnitResults"
Write-Host "  $CpnResults"
Write-Host ""
Write-Host "Open full CPN HTML report:"
Write-Host "  $CpnResults\cpn-report.html"
