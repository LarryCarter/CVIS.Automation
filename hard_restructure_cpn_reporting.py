from pathlib import Path
import shutil
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path.cwd()
PACKAGE_ROOT = Path(__file__).resolve().parent
PAYLOAD = PACKAGE_ROOT / "payload"

def copy_payload() -> None:
    for source in PAYLOAD.rglob("*"):
        if source.is_file():
            relative = source.relative_to(PAYLOAD)
            target = ROOT / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            print(f"Copied {relative}")

def patch_lifecycle_report_names() -> None:
    options = ROOT / "CVIS.Playwright.NUnitCompat" / "Reporting" / "CPNReportOptions.cs"

    if not options.exists():
        print("CPNReportOptions.cs not found; skipped lifecycle rename.")
        return

    text = options.read_text(encoding="utf-8")
    text = text.replace(
        'public string JsonFileName { get; init; } = "cpn-report.json";',
        'public string JsonFileName { get; init; } = "cpn-lifecycle-report.json";')
    text = text.replace(
        'public string HtmlFileName { get; init; } = "cpn-report.html";',
        'public string HtmlFileName { get; init; } = "cpn-lifecycle-report.html";')
    options.write_text(text, encoding="utf-8")
    print("Renamed lifecycle report output to cpn-lifecycle-report.*")

def indent_xml(elem: ET.Element, level: int = 0) -> None:
    space = "\n" + level * "  "

    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = space + "  "

        for child in elem:
            indent_xml(child, level + 1)

        if not elem[-1].tail or not elem[-1].tail.strip():
            elem[-1].tail = space

    if level and (not elem.tail or not elem.tail.strip()):
        elem.tail = space

def add_to_solution() -> None:
    solutions = list(ROOT.glob("*.sln"))

    if not solutions:
        return

    solution = solutions[0]

    projects = [
        ROOT / "CVIS.Playwright.Reporting" / "CVIS.Playwright.Reporting.csproj",
        ROOT / "CVIS.Playwright.Reporting.Tool" / "CVIS.Playwright.Reporting.Tool.csproj",
    ]

    for project in projects:
        if project.exists():
            subprocess.run(
                ["dotnet", "sln", str(solution), "add", str(project)],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True)

def main() -> None:
    patch_lifecycle_report_names()
    copy_payload()
    add_to_solution()

    print("Authoritative reporting restructure applied.")
    print("Run: .\\scripts\\run-authoritative-test-report-local.ps1")
    print("Open: TestResults\\CPN\\cpn-report.html")

if __name__ == "__main__":
    main()
