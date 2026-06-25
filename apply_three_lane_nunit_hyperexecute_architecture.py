from pathlib import Path
import shutil
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path.cwd()
PACKAGE_ROOT = Path(__file__).resolve().parent
PAYLOAD = PACKAGE_ROOT / "payload"

def copy_payload():
    for source in PAYLOAD.rglob("*"):
        if source.is_file():
            relative = source.relative_to(PAYLOAD)
            target = ROOT / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            print(f"Copied {relative}")

def ensure_project_reference(project_path: Path, include: str):
    if not project_path.exists():
        print(f"Project not found, skipped reference: {project_path}")
        return

    tree = ET.parse(project_path)
    root = tree.getroot()

    for reference in root.findall(".//ProjectReference"):
        if reference.attrib.get("Include", "").replace("/", "\\").lower() == include.lower():
            print(f"Reference already exists in {project_path.name}: {include}")
            return

    item_group = None
    for group in root.findall("ItemGroup"):
        item_group = group
        break

    if item_group is None:
        item_group = ET.SubElement(root, "ItemGroup")

    ET.SubElement(item_group, "ProjectReference", {"Include": include})
    indent(root)
    tree.write(project_path, encoding="utf-8", xml_declaration=False)
    print(f"Added ProjectReference to {project_path.name}: {include}")

def indent(element, level=0):
    space = "\n" + level * "  "
    if len(element):
        if not element.text or not element.text.strip():
            element.text = space + "  "
        for child in element:
            indent(child, level + 1)
        if not element[-1].tail or not element[-1].tail.strip():
            element[-1].tail = space
    if level and (not element.tail or not element.tail.strip()):
        element.tail = space

def patch_lifecycle_report_names():
    options = ROOT / "CVIS.Playwright.NUnitCompat" / "Reporting" / "CPNReportOptions.cs"

    if not options.exists():
        print("CPNReportOptions.cs not found; skipped lifecycle report rename.")
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

def add_projects_to_solution():
    solutions = list(ROOT.glob("*.sln"))
    if not solutions:
        print("No .sln found; skipped dotnet sln add.")
        return

    solution = solutions[0]
    projects = [
        ROOT / "CVIS.FunctionalTesting" / "CVIS.FunctionalTesting.csproj",
        ROOT / "CVIS.Playwright.Reporting" / "CVIS.Playwright.Reporting.csproj",
        ROOT / "CVIS.Playwright.Reporting.Tool" / "CVIS.Playwright.Reporting.Tool.csproj",
    ]

    for project in projects:
        if project.exists():
            subprocess.run(["dotnet", "sln", str(solution), "add", str(project)], cwd=ROOT, check=False)

def main():
    patch_lifecycle_report_names()
    copy_payload()

    ensure_project_reference(
        ROOT / "CVIS.Playwright.NUnitCompat" / "CVIS.Playwright.NUnitCompat.csproj",
        r"..\CVIS.FunctionalTesting\CVIS.FunctionalTesting.csproj")

    ensure_project_reference(
        ROOT / "CVIS.Automation.Tests" / "CVIS.Automation.Tests.csproj",
        r"..\CVIS.FunctionalTesting\CVIS.FunctionalTesting.csproj")

    add_projects_to_solution()

    print("")
    print("Three-lane NUnit/HyperExecute architecture applied.")
    print("Run: .\\scripts\\run-cvis-authoritative-report-local.ps1")
    print("Open: TestResults\\CPN\\cpn-report.html")

if __name__ == "__main__":
    main()
