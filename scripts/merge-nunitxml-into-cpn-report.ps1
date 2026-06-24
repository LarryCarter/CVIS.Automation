param(
    [string]$NUnitXmlRoot = ".\TestResults\NUnitXml",
    [string]$CpnRoot = ".\TestResults\CPN",
    [string]$FrameworkName = "CVIS.Playwright.NUnitCompat"
)

$ErrorActionPreference = "Stop"

function HtmlEncode([string]$Value) {
    if ($null -eq $Value) { return "" }
    return [System.Net.WebUtility]::HtmlEncode($Value)
}

function Get-TestStatus([string]$Result, [string]$Label) {
    if ($Result -eq "Passed") { return "Passed" }
    if ($Result -eq "Failed") { return "Failed" }
    if ($Result -eq "Skipped") { return "Skipped" }
    if ($Result -eq "Inconclusive") { return "Inconclusive" }
    if ($Result -eq "Warning") { return "Warning" }
    if ($Label -match "Ignored|Explicit|Cancelled|Skipped") { return "Skipped" }
    return "Unknown"
}

function Get-AttributeValue($Node, [string]$Name) {
    if ($null -eq $Node.Attributes[$Name]) { return "" }
    return $Node.Attributes[$Name].Value
}

$NUnitXmlPath = Resolve-Path -Path $NUnitXmlRoot -ErrorAction SilentlyContinue

if ($null -eq $NUnitXmlPath) {
    throw "NUnit XML folder not found: $NUnitXmlRoot"
}

New-Item -ItemType Directory -Force -Path $CpnRoot | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $CpnRoot "Tests") | Out-Null

$tests = New-Object System.Collections.Generic.List[object]

Get-ChildItem -Path $NUnitXmlPath -Filter "*.xml" -Recurse | ForEach-Object {
    [xml]$xml = Get-Content -Path $_.FullName -Raw

    $nodes = $xml.SelectNodes("//test-case")

    foreach ($node in $nodes) {
        $fullName = Get-AttributeValue $node "fullname"
        if ([string]::IsNullOrWhiteSpace($fullName)) {
            $fullName = Get-AttributeValue $node "name"
        }

        $name = Get-AttributeValue $node "name"
        $result = Get-AttributeValue $node "result"
        $label = Get-AttributeValue $node "label"
        $durationValue = Get-AttributeValue $node "duration"
        $durationMs = 0.0

        if (-not [string]::IsNullOrWhiteSpace($durationValue)) {
            [double]$durationSeconds = 0
            if ([double]::TryParse($durationValue, [ref]$durationSeconds)) {
                $durationMs = [Math]::Round($durationSeconds * 1000, 2)
            }
        }

        $status = Get-TestStatus -Result $result -Label $label

        $message = ""
        $messageNode = $node.SelectSingleNode("failure/message")
        if ($null -eq $messageNode) {
            $messageNode = $node.SelectSingleNode("reason/message")
        }
        if ($null -ne $messageNode) {
            $message = $messageNode.InnerText
        }

        $stackTrace = ""
        $stackNode = $node.SelectSingleNode("failure/stack-trace")
        if ($null -ne $stackNode) {
            $stackTrace = $stackNode.InnerText
        }

        $categories = @()
        $categoryNodes = $node.SelectNodes("properties/property[@name='Category']")
        foreach ($category in $categoryNodes) {
            $value = Get-AttributeValue $category "value"
            if (-not [string]::IsNullOrWhiteSpace($value)) {
                $categories += $value
            }
        }

        $tests.Add([ordered]@{
            Id = ([Guid]::NewGuid().ToString("N"))
            TestName = $name
            FullName = $fullName
            FixtureName = if ($fullName.Contains(".")) { $fullName.Substring(0, $fullName.LastIndexOf(".")) } else { $fullName }
            Status = $status
            DurationMilliseconds = $durationMs
            Message = $message
            StackTrace = $stackTrace
            Categories = $categories
            Source = "NUnitXml"
        })
    }
}

$total = $tests.Count
$passed = ($tests | Where-Object { $_.Status -eq "Passed" }).Count
$failed = ($tests | Where-Object { $_.Status -eq "Failed" }).Count
$skipped = ($tests | Where-Object { $_.Status -eq "Skipped" }).Count
$other = $total - $passed - $failed - $skipped

$summary = [ordered]@{
    Framework = $FrameworkName
    GeneratedUtc = [DateTimeOffset]::UtcNow.ToString("O")
    Source = "NUnitXml"
    Total = $total
    Passed = $passed
    Failed = $failed
    Skipped = $skipped
    Other = $other
    Tests = $tests
}

$jsonPath = Join-Path $CpnRoot "cpn-report.json"
$allJsonPath = Join-Path $CpnRoot "cpn-report-all-tests.json"
$htmlPath = Join-Path $CpnRoot "cpn-report.html"
$allHtmlPath = Join-Path $CpnRoot "cpn-report-all-tests.html"

$summary | ConvertTo-Json -Depth 20 | Set-Content -Path $jsonPath -Encoding UTF8
$summary | ConvertTo-Json -Depth 20 | Set-Content -Path $allJsonPath -Encoding UTF8

$testRows = New-Object System.Text.StringBuilder

foreach ($test in ($tests | Sort-Object Status, FullName)) {
    $message = HtmlEncode $test.Message
    if (-not [string]::IsNullOrWhiteSpace($test.StackTrace)) {
        $message = $message + "<details><summary>Stack trace</summary><pre>" + (HtmlEncode $test.StackTrace) + "</pre></details>"
    }

    [void]$testRows.AppendLine("<tr>")
    [void]$testRows.AppendLine("<td class=`"$($test.Status)`">$(HtmlEncode $test.Status)</td>")
    [void]$testRows.AppendLine("<td><code>$(HtmlEncode $test.FullName)</code></td>")
    [void]$testRows.AppendLine("<td>$(HtmlEncode ([string]$test.DurationMilliseconds)) ms</td>")
    [void]$testRows.AppendLine("<td>$message</td>")
    [void]$testRows.AppendLine("</tr>")

    $safeName = ($test.FullName -replace '[\\/:*?"<>|]', '_')
    if ($safeName.Length -gt 150) {
        $safeName = $safeName.Substring(0, 150)
    }

    $test | ConvertTo-Json -Depth 20 | Set-Content -Path (Join-Path $CpnRoot "Tests\$safeName.json") -Encoding UTF8
}

$html = @"
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>CPN Test Report</title>
<style>
body{font-family:Segoe UI,Arial,sans-serif;margin:24px;background:#f7f7f8;color:#1f2328;}
h1{margin-bottom:4px;}
.meta{color:#57606a;margin-bottom:18px;}
.cards{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:24px;}
.card{background:white;border:1px solid #d0d7de;border-radius:8px;padding:14px 22px;min-width:120px;}
.number{font-size:30px;font-weight:700;}
table{width:100%;border-collapse:collapse;background:white;border:1px solid #d0d7de;}
th,td{text-align:left;border-bottom:1px solid #d8dee4;padding:10px;vertical-align:top;}
th{background:#f1f3f5;}
.Passed{color:#1a7f37;font-weight:700;}
.Failed{color:#cf222e;font-weight:700;}
.Skipped,.Inconclusive,.Warning,.Unknown{color:#9a6700;font-weight:700;}
code{font-family:Consolas,monospace;font-size:12px;}
pre{white-space:pre-wrap;}
</style>
</head>
<body>
<h1>CPN Test Report</h1>
<div class="meta">Framework: $(HtmlEncode $FrameworkName) | Source: NUnit XML | Generated UTC: $(HtmlEncode $summary.GeneratedUtc)</div>
<div class="cards">
  <div class="card"><div class="number">$total</div><div>Total</div></div>
  <div class="card"><div class="number">$passed</div><div>Passed</div></div>
  <div class="card"><div class="number">$failed</div><div>Failed</div></div>
  <div class="card"><div class="number">$skipped</div><div>Skipped</div></div>
  <div class="card"><div class="number">$other</div><div>Other</div></div>
</div>
<table>
<thead><tr><th>Status</th><th>Test</th><th>Duration</th><th>Message</th></tr></thead>
<tbody>
$($testRows.ToString())
</tbody>
</table>
</body>
</html>
"@

$html | Set-Content -Path $htmlPath -Encoding UTF8
$html | Set-Content -Path $allHtmlPath -Encoding UTF8

Write-Host "Created full CPN report from NUnit XML:"
Write-Host "  $htmlPath"
Write-Host "  $jsonPath"
Write-Host "Total: $total Passed: $passed Failed: $failed Skipped: $skipped Other: $other"
