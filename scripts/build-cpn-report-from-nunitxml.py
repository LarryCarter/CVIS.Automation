from __future__ import annotations

import argparse
import html
import json
import os
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path


def status_from(result: str | None, label: str | None) -> str:
    result = result or ""
    label = label or ""

    if result in {"Passed", "Failed", "Skipped", "Inconclusive", "Warning"}:
        return result

    if re.search(r"Ignored|Explicit|Cancelled|Skipped", label, re.I):
        return "Skipped"

    return "Unknown"


def fixture_name(full_name: str) -> str:
    if "." not in full_name:
        return full_name
    return full_name.rsplit(".", 1)[0]


def read_message(node: ET.Element) -> tuple[str, str]:
    message = ""
    stack_trace = ""

    failure = node.find("failure")
    reason = node.find("reason")

    if failure is not None:
        message_node = failure.find("message")
        stack_node = failure.find("stack-trace")
        if message_node is not None and message_node.text:
            message = message_node.text
        if stack_node is not None and stack_node.text:
            stack_trace = stack_node.text

    if not message and reason is not None:
        message_node = reason.find("message")
        if message_node is not None and message_node.text:
            message = message_node.text

    return message, stack_trace


def categories(node: ET.Element) -> list[str]:
    values: list[str] = []
    properties = node.find("properties")
    if properties is None:
        return values

    for prop in properties.findall("property"):
        if prop.attrib.get("name") == "Category":
            value = prop.attrib.get("value")
            if value:
                values.append(value)

    return sorted(set(values), key=str.lower)


def parse_nunit_xml(xml_root: Path) -> list[dict]:
    tests: list[dict] = []

    for path in sorted(xml_root.rglob("*.xml")):
        try:
            tree = ET.parse(path)
        except ET.ParseError:
            continue

        root = tree.getroot()

        for node in root.findall(".//test-case"):
            name = node.attrib.get("name", "")
            full_name = node.attrib.get("fullname") or name
            result = node.attrib.get("result")
            label = node.attrib.get("label")
            status = status_from(result, label)
            duration_seconds = 0.0

            try:
                duration_seconds = float(node.attrib.get("duration", "0") or "0")
            except ValueError:
                duration_seconds = 0.0

            message, stack_trace = read_message(node)

            tests.append({
                "id": f"{len(tests) + 1:06d}",
                "testName": name,
                "fullName": full_name,
                "fixtureName": fixture_name(full_name),
                "status": status,
                "durationMilliseconds": round(duration_seconds * 1000, 2),
                "message": message,
                "stackTrace": stack_trace,
                "categories": categories(node),
                "sourceXml": str(path),
            })

    return tests


def write_report(tests: list[dict], output_root: Path, framework_name: str) -> None:
    output_root.mkdir(parents=True, exist_ok=True)
    tests_root = output_root / "Tests"
    tests_root.mkdir(parents=True, exist_ok=True)

    total = len(tests)
    passed = sum(1 for item in tests if item["status"] == "Passed")
    failed = sum(1 for item in tests if item["status"] == "Failed")
    skipped = sum(1 for item in tests if item["status"] == "Skipped")
    other = total - passed - failed - skipped

    summary = {
        "framework": framework_name,
        "source": "NUnitXml",
        "generatedUtc": datetime.now(timezone.utc).isoformat(),
        "total": total,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "other": other,
        "tests": tests,
    }

    (output_root / "cpn-report.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )
    (output_root / "cpn-report-all-tests.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )

    for item in tests:
        safe = re.sub(r'[\\/:*?"<>|]', "_", item["fullName"])[:150]
        (tests_root / f"{safe}.json").write_text(
            json.dumps(item, indent=2),
            encoding="utf-8",
        )

    rows = []
    for item in sorted(tests, key=lambda value: (value["status"], value["fullName"])):
        message = html.escape(item.get("message") or "")
        stack_trace = item.get("stackTrace") or ""
        if stack_trace:
            message += (
                "<details><summary>Stack trace</summary><pre>"
                + html.escape(stack_trace)
                + "</pre></details>"
            )

        rows.append(
            "<tr>"
            f"<td class=\"{html.escape(item['status'])}\">{html.escape(item['status'])}</td>"
            f"<td><code>{html.escape(item['fullName'])}</code></td>"
            f"<td>{html.escape(str(item['durationMilliseconds']))} ms</td>"
            f"<td>{message}</td>"
            "</tr>"
        )

    html_report = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>CPN Full Test Report</title>
<style>
body{{font-family:Segoe UI,Arial,sans-serif;margin:24px;background:#f7f7f8;color:#1f2328;}}
h1{{margin-bottom:4px;}}
.meta{{color:#57606a;margin-bottom:18px;}}
.cards{{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:24px;}}
.card{{background:white;border:1px solid #d0d7de;border-radius:8px;padding:14px 22px;min-width:120px;}}
.number{{font-size:30px;font-weight:700;}}
table{{width:100%;border-collapse:collapse;background:white;border:1px solid #d0d7de;}}
th,td{{text-align:left;border-bottom:1px solid #d8dee4;padding:10px;vertical-align:top;}}
th{{background:#f1f3f5;}}
.Passed{{color:#1a7f37;font-weight:700;}}
.Failed{{color:#cf222e;font-weight:700;}}
.Skipped,.Inconclusive,.Warning,.Unknown{{color:#9a6700;font-weight:700;}}
code{{font-family:Consolas,monospace;font-size:12px;}}
pre{{white-space:pre-wrap;}}
</style>
</head>
<body>
<h1>CPN Full Test Report</h1>
<div class="meta">Framework: {html.escape(framework_name)} | Source: NUnit XML | Generated UTC: {html.escape(summary["generatedUtc"])}</div>
<div class="cards">
  <div class="card"><div class="number">{total}</div><div>Total</div></div>
  <div class="card"><div class="number">{passed}</div><div>Passed</div></div>
  <div class="card"><div class="number">{failed}</div><div>Failed</div></div>
  <div class="card"><div class="number">{skipped}</div><div>Skipped</div></div>
  <div class="card"><div class="number">{other}</div><div>Other</div></div>
</div>
<table>
<thead><tr><th>Status</th><th>Test</th><th>Duration</th><th>Message</th></tr></thead>
<tbody>
{os.linesep.join(rows)}
</tbody>
</table>
</body>
</html>
"""

    (output_root / "cpn-report.html").write_text(html_report, encoding="utf-8")
    (output_root / "cpn-report-all-tests.html").write_text(html_report, encoding="utf-8")

    (output_root / "cpn-report-summary.txt").write_text(
        (
            f"Framework: {framework_name}\n"
            f"Source: NUnitXml\n"
            f"Total: {total}\n"
            f"Passed: {passed}\n"
            f"Failed: {failed}\n"
            f"Skipped: {skipped}\n"
            f"Other: {other}\n"
        ),
        encoding="utf-8",
    )

    print(f"Created {output_root / 'cpn-report.html'}")
    print(f"Total: {total} Passed: {passed} Failed: {failed} Skipped: {skipped} Other: {other}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--nunit-xml-root", required=True)
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--framework-name", default="CVIS.Automation.Tests")
    parser.add_argument("--minimum-total", type=int, default=1)
    args = parser.parse_args()

    xml_root = Path(args.nunit_xml_root)
    output_root = Path(args.output_root)

    if not xml_root.exists():
        raise SystemExit(f"NUnit XML folder does not exist: {xml_root}")

    tests = parse_nunit_xml(xml_root)

    if len(tests) < args.minimum_total:
        raise SystemExit(
            f"NUnit XML only contained {len(tests)} tests, expected at least {args.minimum_total}."
        )

    write_report(tests, output_root, args.framework_name)


if __name__ == "__main__":
    main()
