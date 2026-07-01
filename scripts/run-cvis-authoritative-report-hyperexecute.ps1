param(
    [string]$Configuration = "Debug",
    [int]$MinimumTotal = 250
)

$ErrorActionPreference = "Continue"

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

$TestProjects = Get-ChildItem -Path $Root -Recurse -Filter "*.csproj" |
    Where-Object {
        $_.FullName -notmatch "\\bin\\" -and
        $_.FullName -notmatch "\\obj\\" -and
        (
            $_.Name -like "*.Tests.csproj" -or
            (Select-String -Path $_.FullName -Pattern "<IsTestProject>true</IsTestProject>" -SimpleMatch -Quiet)
        )
    } |
    Sort-Object FullName

if ($TestProjects.Count -eq 0) {
    throw "No test projects found."
}

$testRunFailed = $false

foreach ($Project in $TestProjects) {
    $ProjectName = [System.IO.Path]::GetFileNameWithoutExtension($Project.FullName)
    $ProjectTrx = Join-Path $TrxResults $ProjectName
    $ProjectNUnitXml = Join-Path $NUnitXmlResults $ProjectName

    New-Item -ItemType Directory -Force -Path $ProjectTrx | Out-Null
    New-Item -ItemType Directory -Force -Path $ProjectNUnitXml | Out-Null

    Write-Host ""
    Write-Host "Running $ProjectName"

    dotnet test "$($Project.FullName)" `
        --configuration $Configuration `
        --logger "trx;LogFileName=$ProjectName.trx" `
        --results-directory "$ProjectTrx" `
        -- NUnit.TestOutputXml="$ProjectNUnitXml"

    if ($LASTEXITCODE -ne 0) {
        $testRunFailed = $true
        Write-Warning "$ProjectName returned exit code $LASTEXITCODE"
    }
}

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
Get-Content (Join-Path $CpnResults "cpn-report-summary.txt")

if ($testRunFailed -or $reportExitCode -ne 0) {
    exit 1
}

exit 0
