from __future__ import annotations
import argparse
import html
import json
import os
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

def duration_to_ms(value):
    if not value:
        return 0.0
    try:
        parts = value.split(":")
        if len(parts) == 3:
            return round((float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])) * 1000, 2)
    except Exception:
        pass
    return 0.0

def seconds_to_ms(value):
    try:
        return round(float(value or "0") * 1000, 2)
    except Exception:
        return 0.0

def fixture_name(full_name):
    return full_name.rsplit(".", 1)[0] if "." in full_name else full_name

def status_from_nunit(result, label):
    if result in {"Passed", "Failed", "Skipped", "Inconclusive", "Warning"}:
        return result
    if label and re.search(r"Ignored|Explicit|Cancelled|Skipped", label, re.I):
        return "Skipped"
    return "Unknown"

def parse_trx(root_dir: Path):
    tests = []
    for p in sorted(root_dir.rglob("*.trx")):
        try:
            root = ET.parse(p).getroot()
        except ET.ParseError:
            continue
        ns_match = re.match(r"\{.*\}", root.tag)
        ns = ns_match.group(0) if ns_match else ""
        defs = {}
        for ut in root.findall(f".//{ns}UnitTest"):
            tid = ut.attrib.get("id", "")
            tm = ut.find(f".//{ns}TestMethod")
            name = ut.attrib.get("name", "")
            cls = ""
            if tm is not None:
                cls = tm.attrib.get("className", "")
                name = tm.attrib.get("name", name)
            full = f"{cls}.{name}".strip(".") if cls else name
            defs[tid] = {"name": name, "full": full}
        for r in root.findall(f".//{ns}UnitTestResult"):
            tid = r.attrib.get("testId", "")
            d = defs.get(tid, {})
            outcome = r.attrib.get("outcome", "Unknown")
            status = {
                "Passed": "Passed",
                "Failed": "Failed",
                "NotExecuted": "Skipped",
                "Timeout": "Failed",
                "Aborted": "Failed",
                "Error": "Failed",
                "Inconclusive": "Inconclusive",
            }.get(outcome, outcome)
            full = d.get("full") or r.attrib.get("testName") or tid or "Unknown"
            name = d.get("name") or r.attrib.get("testName") or full
            msg_node = r.find(f".//{ns}Message")
            st_node = r.find(f".//{ns}StackTrace")
            tests.append({
                "id": f"trx-{len(tests) + 1:06d}",
                "testName": name,
                "fullName": full,
                "fixtureName": fixture_name(full),
                "status": status,
                "durationMilliseconds": duration_to_ms(r.attrib.get("duration")),
                "message": msg_node.text if msg_node is not None and msg_node.text else "",
                "stackTrace": st_node.text if st_node is not None and st_node.text else "",
                "categories": [],
                "source": "TRX",
                "sourceFile": str(p),
            })
    return tests

def parse_nunit(root_dir: Path):
    tests = []
    for p in sorted(root_dir.rglob("*.xml")):
        try:
            root = ET.parse(p).getroot()
        except ET.ParseError:
            continue
        for n in root.findall(".//test-case"):
            name = n.attrib.get("name", "")
            full = n.attrib.get("fullname") or name
            msg = ""
            stack = ""
            failure = n.find("failure")
            reason = n.find("reason")
            if failure is not None:
                mn = failure.find("message")
                sn = failure.find("stack-trace")
                msg = mn.text if mn is not None and mn.text else ""
                stack = sn.text if sn is not None and sn.text else ""
            if not msg and reason is not None:
                mn = reason.find("message")
                msg = mn.text if mn is not None and mn.text else ""
            cats = []
            props = n.find("properties")
            if props is not None:
                for prop in props.findall("property"):
                    if prop.attrib.get("name") == "Category" and prop.attrib.get("value"):
                        cats.append(prop.attrib["value"])
            tests.append({
                "id": f"nunit-{len(tests) + 1:06d}",
                "testName": name,
                "fullName": full,
                "fixtureName": fixture_name(full),
                "status": status_from_nunit(n.attrib.get("result"), n.attrib.get("label")),
                "durationMilliseconds": seconds_to_ms(n.attrib.get("duration")),
                "message": msg,
                "stackTrace": stack,
                "categories": sorted(set(cats), key=str.lower),
                "source": "NUnitXml",
                "sourceFile": str(p),
            })
    return tests

def dedupe(tests):
    result = {}
    for test in sorted(tests, key=lambda x: 0 if x.get("source") == "TRX" else 1):
        result.setdefault(test["fullName"], test)
    return list(result.values())

def write_report(tests, output: Path, framework):
    output.mkdir(parents=True, exist_ok=True)
    (output / "Tests").mkdir(parents=True, exist_ok=True)
    total = len(tests)
    passed = sum(1 for t in tests if t["status"] == "Passed")
    failed = sum(1 for t in tests if t["status"] == "Failed")
    skipped = sum(1 for t in tests if t["status"] == "Skipped")
    other = total - passed - failed - skipped
    summary = {
        "framework": framework,
        "source": "TRX+NUnitXml",
        "generatedUtc": datetime.now(timezone.utc).isoformat(),
        "total": total,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "other": other,
        "tests": sorted(tests, key=lambda x: x["fullName"]),
    }
    for file_name in ["cpn-report.json", "cpn-report-all-tests.json"]:
        (output / file_name).write_text(json.dumps(summary, indent=2), encoding="utf-8")
    rows = []
    for test in sorted(tests, key=lambda x: (x["status"], x["fullName"])):
        message = html.escape(test.get("message") or "")
        if test.get("stackTrace"):
            message += "<details><summary>Stack trace</summary><pre>" + html.escape(test["stackTrace"]) + "</pre></details>"
        rows.append(
            "<tr>"
            f"<td class='{html.escape(test['status'])}'>{html.escape(test['status'])}</td>"
            f"<td><code>{html.escape(test['fullName'])}</code></td>"
            f"<td>{html.escape(str(test['durationMilliseconds']))} ms</td>"
            f"<td>{html.escape(test.get('source', ''))}</td>"
            f"<td>{message}</td>"
            "</tr>"
        )
        safe = re.sub(r'[\\/:*?"<>|]', "_", test["fullName"])[:150]
        (output / "Tests" / f"{safe}.json").write_text(json.dumps(test, indent=2), encoding="utf-8")
    page = """<!doctype html>
<html lang='en'>
<head>
<meta charset='utf-8' />
<meta name='viewport' content='width=device-width, initial-scale=1' />
<title>CPN Full Test Report</title>
<style>
body{font-family:Segoe UI,Arial,sans-serif;margin:24px;background:#f7f7f8;color:#1f2328;}
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
<h1>CPN Full Test Report</h1>
<div>Framework: __FRAMEWORK__ | Source: TRX + NUnit XML | Generated UTC: __UTC__</div>
<div class='cards'>
  <div class='card'><div class='number'>__TOTAL__</div><div>Total</div></div>
  <div class='card'><div class='number'>__PASSED__</div><div>Passed</div></div>
  <div class='card'><div class='number'>__FAILED__</div><div>Failed</div></div>
  <div class='card'><div class='number'>__SKIPPED__</div><div>Skipped</div></div>
  <div class='card'><div class='number'>__OTHER__</div><div>Other</div></div>
</div>
<table>
<thead><tr><th>Status</th><th>Test</th><th>Duration</th><th>Source</th><th>Message</th></tr></thead>
<tbody>
__ROWS__
</tbody>
</table>
</body>
</html>
"""
    page = (page
        .replace("__FRAMEWORK__", html.escape(framework))
        .replace("__UTC__", html.escape(summary["generatedUtc"]))
        .replace("__TOTAL__", str(total))
        .replace("__PASSED__", str(passed))
        .replace("__FAILED__", str(failed))
        .replace("__SKIPPED__", str(skipped))
        .replace("__OTHER__", str(other))
        .replace("__ROWS__", os.linesep.join(rows)))
    for file_name in ["cpn-report.html", "cpn-report-all-tests.html"]:
        (output / file_name).write_text(page, encoding="utf-8")
    (output / "cpn-report-summary.txt").write_text(
        f"Framework: {framework}\nSource: TRX+NUnitXml\nTotal: {total}\nPassed: {passed}\nFailed: {failed}\nSkipped: {skipped}\nOther: {other}\n",
        encoding="utf-8",
    )
    print(f"Created {output / 'cpn-report.html'}")
    print(f"Total: {total} Passed: {passed} Failed: {failed} Skipped: {skipped} Other: {other}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trx-root", required=True)
    parser.add_argument("--nunit-xml-root", required=True)
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--framework-name", default="CVIS Full Test Run")
    parser.add_argument("--minimum-total", type=int, default=250)
    args = parser.parse_args()
    tests = dedupe(parse_trx(Path(args.trx_root)) + parse_nunit(Path(args.nunit_xml_root)))
    if len(tests) < args.minimum_total:
        raise SystemExit(f"Report only found {len(tests)} tests. Expected at least {args.minimum_total}. TRX root: {args.trx_root}; NUnit XML root: {args.nunit_xml_root}")
    write_report(tests, Path(args.output_root), args.framework_name)

if __name__ == "__main__":
    main()
