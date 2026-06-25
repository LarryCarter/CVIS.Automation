param(
    [string]$Configuration = "Debug",
    [int]$MinimumTotal = 250
)

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$TestResults = Join-Path $Root "TestResults"
$CpnResults = Join-Path $TestResults "CPN"
$TrxResults = Join-Path $TestResults "TRX"
$NUnitXmlResults = Join-Path $TestResults "NUnitXml"

if (Test-Path $TestResults) {
    Remove-Item $TestResults -Recurse -Force
}

New-Item -ItemType Directory -Force -Path $CpnResults | Out-Null
New-Item -ItemType Directory -Force -Path $TrxResults | Out-Null
New-Item -ItemType Directory -Force -Path $NUnitXmlResults | Out-Null

$Projects = @(
    "$Root\CVIS.Automation.Tests\CVIS.Automation.Tests.csproj",
    "$Root\CVIS.Playwright.NUnitCompat.Tests\CVIS.Playwright.NUnitCompat.Tests.csproj"
)

foreach ($Project in $Projects) {
    if (-not (Test-Path $Project)) {
        Write-Host "Skipping missing test project: $Project"
        continue
    }

    $ProjectName = [System.IO.Path]::GetFileNameWithoutExtension($Project)
    $ProjectTrx = Join-Path $TrxResults $ProjectName
    $ProjectNUnitXml = Join-Path $NUnitXmlResults $ProjectName

    New-Item -ItemType Directory -Force -Path $ProjectTrx | Out-Null
    New-Item -ItemType Directory -Force -Path $ProjectNUnitXml | Out-Null

    Write-Host ""
    Write-Host "Running $ProjectName"

    dotnet test $Project `
        --configuration $Configuration `
        --logger "trx;LogFileName=$ProjectName.trx" `
        --results-directory "$ProjectTrx" `
        -- NUnit.TestOutputXml="$ProjectNUnitXml"
}

dotnet run --project "$Root\CVIS.Playwright.Reporting.Tool\CVIS.Playwright.Reporting.Tool.csproj" -- `
    --trx-root "$TrxResults" `
    --nunit-xml-root "$NUnitXmlResults" `
    --output-root "$CpnResults" `
    --framework-name "CVIS Authoritative Test Run" `
    --minimum-total "$MinimumTotal"

Write-Host ""
Write-Host "AUTHORITATIVE REPORT:"
Write-Host "  $CpnResults\cpn-report.html"
Write-Host ""
Get-Content (Join-Path $CpnResults "cpn-report-summary.txt")
