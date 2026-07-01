from pathlib import Path
import shutil
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path.cwd()

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

def ensure_package_reference(project_path: Path, include: str):
    if not project_path.exists():
        print(f"Skipped missing project: {project_path}")
        return

    tree = ET.parse(project_path)
    root = tree.getroot()

    for package in root.findall(".//PackageReference"):
        if package.attrib.get("Include", "").lower() == include.lower():
            return

    item_group = root.find("ItemGroup")
    if item_group is None:
        item_group = ET.SubElement(root, "ItemGroup")

    ET.SubElement(item_group, "PackageReference", {"Include": include})
    indent(root)
    tree.write(project_path, encoding="utf-8", xml_declaration=False)
    print(f"Added PackageReference {include} to {project_path}")

def ensure_project_reference(project_path: Path, include: str):
    if not project_path.exists():
        print(f"Skipped missing project: {project_path}")
        return

    tree = ET.parse(project_path)
    root = tree.getroot()
    target = include.replace("/", "\\").lower()

    for reference in root.findall(".//ProjectReference"):
        existing = reference.attrib.get("Include", "").replace("/", "\\").lower()
        if existing == target:
            return

    item_group = root.find("ItemGroup")
    if item_group is None:
        item_group = ET.SubElement(root, "ItemGroup")

    ET.SubElement(item_group, "ProjectReference", {"Include": include})
    indent(root)
    tree.write(project_path, encoding="utf-8", xml_declaration=False)
    print(f"Added ProjectReference {include} to {project_path}")

def patch_lifecycle_report_names():
    options = ROOT / "CVIS.Playwright.NUnitCompat" / "Reporting" / "CPNReportOptions.cs"

    if not options.exists():
        return

    text = options.read_text(encoding="utf-8")
    text = text.replace('"cpn-report.json"', '"cpn-lifecycle-report.json"')
    text = text.replace('"cpn-report.html"', '"cpn-lifecycle-report.html"')
    options.write_text(text, encoding="utf-8")
    print("Ensured lifecycle report names are cpn-lifecycle-report.*")

def remove_accidental_payload_folder():
    payload = ROOT / "payload"
    if payload.exists():
        shutil.rmtree(payload)
        print("Removed accidental payload/ folder from repository root.")

def add_projects_to_solution():
    solutions = list(ROOT.glob("*.sln"))
    if not solutions:
        return

    solution = solutions[0]

    for project in [
        ROOT / "CVIS.FunctionalTesting" / "CVIS.FunctionalTesting.csproj",
        ROOT / "CVIS.Playwright.Reporting" / "CVIS.Playwright.Reporting.csproj",
        ROOT / "CVIS.Playwright.Reporting.Tool" / "CVIS.Playwright.Reporting.Tool.csproj",
    ]:
        if project.exists():
            subprocess.run(["dotnet", "sln", str(solution), "add", str(project)], cwd=ROOT, check=False)

def main():
    remove_accidental_payload_folder()
    patch_lifecycle_report_names()

    ensure_package_reference(
        ROOT / "CVIS.FunctionalTesting" / "CVIS.FunctionalTesting.csproj",
        "Microsoft.Data.SqlClient")

    ensure_project_reference(
        ROOT / "CVIS.Automation.Tests" / "CVIS.Automation.Tests.csproj",
        r"..\CVIS.FunctionalTesting\CVIS.FunctionalTesting.csproj")

    ensure_project_reference(
        ROOT / "CVIS.Playwright.NUnitCompat" / "CVIS.Playwright.NUnitCompat.csproj",
        r"..\CVIS.FunctionalTesting\CVIS.FunctionalTesting.csproj")

    add_projects_to_solution()

    print("Applied CVIS Automation direct base-class/docs package.")

if __name__ == "__main__":
    main()
