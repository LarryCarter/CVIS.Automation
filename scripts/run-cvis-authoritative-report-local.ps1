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

$ExcludedPathFragments = @(
    "\.contollo\",
    "\bin\",
    "\obj\",
    "\payload\",
    "\TestResults\"
)

$Projects = Get-ChildItem -Path $Root -Recurse -Filter "*.csproj" |
    Where-Object {
        $fullName = $_.FullName
        $isTestProject = $_.BaseName.EndsWith(".Tests")
        $isExcluded = $false

        foreach ($fragment in $ExcludedPathFragments) {
            if ($fullName -match [regex]::Escape($fragment)) {
                $isExcluded = $true
                break
            }
        }

        $isTestProject -and -not $isExcluded
    } |
    Sort-Object FullName

if (-not $Projects -or $Projects.Count -eq 0) {
    throw "No NUnit test projects were discovered. Expected one or more *.Tests.csproj files."
}

$testRunFailed = $false

foreach ($Project in $Projects) {
    $ProjectName = [System.IO.Path]::GetFileNameWithoutExtension($Project.FullName)
    $ProjectTrx = Join-Path $TrxResults $ProjectName
    $ProjectNUnitXml = Join-Path $NUnitXmlResults $ProjectName

    New-Item -ItemType Directory -Force -Path $ProjectTrx | Out-Null
    New-Item -ItemType Directory -Force -Path $ProjectNUnitXml | Out-Null

    Write-Host ""
    Write-Host "Running $ProjectName"

    dotnet test $Project.FullName `
        --configuration $Configuration `
        --logger "trx;LogFileName=$ProjectName.trx" `
        --results-directory "$ProjectTrx" `
        -- NUnit.TestOutputXml="$ProjectNUnitXml"

    if ($LASTEXITCODE -ne 0) {
        $testRunFailed = $true
    }
}

$reportExitCode = 0

dotnet run --project "$Root\CVIS.Playwright.Reporting.Tool\CVIS.Playwright.Reporting.Tool.csproj" -- `
    --trx-root "$TrxResults" `
    --nunit-xml-root "$NUnitXmlResults" `
    --output-root "$CpnResults" `
    --framework-name "CVIS Authoritative Test Run" `
    --minimum-total "$MinimumTotal"

$reportExitCode = $LASTEXITCODE

Write-Host ""
Write-Host "AUTHORITATIVE REPORT:"
Write-Host "  $CpnResults\cpn-report.html"
Write-Host ""

$summaryPath = Join-Path $CpnResults "cpn-report-summary.txt"
if (Test-Path $summaryPath) {
    Get-Content $summaryPath
}

if ($testRunFailed -or $reportExitCode -ne 0) {
    exit 1
}

exit 0
