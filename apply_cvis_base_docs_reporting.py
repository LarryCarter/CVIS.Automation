from pathlib import Path
import shutil, subprocess, xml.etree.ElementTree as ET

ROOT = Path.cwd()
PAYLOAD = Path(__file__).resolve().parent / "payload"

def copy_payload():
    for src in PAYLOAD.rglob("*"):
        if src.is_file():
            rel = src.relative_to(PAYLOAD)
            dst = ROOT / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print(f"Copied {rel}")

def remove_payload_folder():
    d = ROOT / "payload"
    if d.exists():
        shutil.rmtree(d)
        print("Removed repository payload/ folder.")

def indent(e, level=0):
    space = "\n" + level * "  "
    if len(e):
        if not e.text or not e.text.strip():
            e.text = space + "  "
        for child in e:
            indent(child, level + 1)
        if not e[-1].tail or not e[-1].tail.strip():
            e[-1].tail = space
    if level and (not e.tail or not e.tail.strip()):
        e.tail = space

def ensure_package(project, include):
    project = Path(project)
    if not project.exists():
        return
    tree = ET.parse(project)
    root = tree.getroot()
    for p in root.findall(".//PackageReference"):
        if p.attrib.get("Include", "").lower() == include.lower():
            return
    group = root.find("ItemGroup") or ET.SubElement(root, "ItemGroup")
    ET.SubElement(group, "PackageReference", {"Include": include})
    indent(root)
    tree.write(project, encoding="utf-8", xml_declaration=False)
    print(f"Added PackageReference {include} to {project}")

def ensure_project_ref(project, include):
    project = Path(project)
    if not project.exists():
        return
    tree = ET.parse(project)
    root = tree.getroot()
    target = include.replace("/", "\\").lower()
    for r in root.findall(".//ProjectReference"):
        if r.attrib.get("Include", "").replace("/", "\\").lower() == target:
            return
    group = root.find("ItemGroup") or ET.SubElement(root, "ItemGroup")
    ET.SubElement(group, "ProjectReference", {"Include": include})
    indent(root)
    tree.write(project, encoding="utf-8", xml_declaration=False)
    print(f"Added ProjectReference {include} to {project}")

def patch_lifecycle_names():
    path = ROOT / "CVIS.Playwright.NUnitCompat/Reporting/CPNReportOptions.cs"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    text = text.replace('"cpn-report.json"', '"cpn-lifecycle-report.json"')
    text = text.replace('"cpn-report.html"', '"cpn-lifecycle-report.html"')
    path.write_text(text, encoding="utf-8")
    print("Ensured lifecycle report names are separate.")

def main():
    remove_payload_folder()
    patch_lifecycle_names()
    copy_payload()
    ensure_package(ROOT / "CVIS.FunctionalTesting/CVIS.FunctionalTesting.csproj", "Microsoft.Data.SqlClient")
    ensure_project_ref(ROOT / "CVIS.Automation.Tests/CVIS.Automation.Tests.csproj", r"..\CVIS.FunctionalTesting\CVIS.FunctionalTesting.csproj")
    ensure_project_ref(ROOT / "CVIS.Playwright.NUnitCompat/CVIS.Playwright.NUnitCompat.csproj", r"..\CVIS.FunctionalTesting\CVIS.FunctionalTesting.csproj")
    slns = list(ROOT.glob("*.sln"))
    if slns:
        for project in [
            ROOT / "CVIS.FunctionalTesting/CVIS.FunctionalTesting.csproj",
            ROOT / "CVIS.Playwright.Reporting/CVIS.Playwright.Reporting.csproj",
            ROOT / "CVIS.Playwright.Reporting.Tool/CVIS.Playwright.Reporting.Tool.csproj",
        ]:
            if project.exists():
                subprocess.run(["dotnet", "sln", str(slns[0]), "add", str(project)], cwd=ROOT, check=False)
    print("CVIS base-class docs and dynamic reporting applied.")

if __name__ == "__main__":
    main()
