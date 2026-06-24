param(
    [string]$Configuration = "Debug",
    [int]$MinimumTotal = 250
)

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
    $ProjectNUnitResults = Join-Path $NUnitResults $ProjectName
    $ProjectNUnitXmlResults = Join-Path $NUnitXmlResults $ProjectName

    New-Item -ItemType Directory -Force -Path $ProjectNUnitResults | Out-Null
    New-Item -ItemType Directory -Force -Path $ProjectNUnitXmlResults | Out-Null

    Write-Host ""
    Write-Host "Running $ProjectName"

    dotnet test $Project `
        --configuration $Configuration `
        --logger "trx;LogFileName=$ProjectName.trx" `
        --results-directory "$ProjectNUnitResults" `
        -- NUnit.TestOutputXml="$ProjectNUnitXmlResults"
}

python "$Root\scripts\build-cpn-report-from-nunitxml.py" `
    --nunit-xml-root "$NUnitXmlResults" `
    --output-root "$CpnResults" `
    --framework-name "CVIS Full NUnit Run" `
    --minimum-total $MinimumTotal

Write-Host ""
Write-Host "AUTHORITATIVE HYPEREXECUTE INPUT:"
Write-Host "  $NUnitXmlResults"
Write-Host ""
Write-Host "FULL CPN HTML REPORT:"
Write-Host "  $CpnResults\cpn-report.html"
Write-Host ""
Write-Host "SUMMARY:"
Get-Content (Join-Path $CpnResults "cpn-report-summary.txt")
