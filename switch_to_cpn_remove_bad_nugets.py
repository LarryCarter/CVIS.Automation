r"""
CVIS RDEL Update Script
Package: Switch To CPN Remove Bad NuGets

Purpose:
    - Remove packages we should not use:
        Microsoft.Playwright.NUnit
        System.Text.Json explicit package reference
        xUnit packages
    - Ensure projects use:
        Microsoft.Playwright
        NUnit
        CPN project reference
    - Replace Microsoft.Playwright.NUnit usings/inheritance with CPN equivalents.
    - Update appsettings.test.json DB connection string.

Run from solution root:
    C:\Users\larry\source\repos\CVIS.Automation
"""

from __future__ import annotations

from pathlib import Path
import json
import re
import xml.etree.ElementTree as ET


ROOT = Path.cwd()

FORBIDDEN_PACKAGES = {
    "Microsoft.Playwright.NUnit",
    "System.Text.Json",
    "xunit",
    "xunit.runner.visualstudio",
    "xunit.analyzers",
    "xunit.assert",
    "xunit.core",
    "xunit.extensibility.core",
    "xunit.extensibility.execution",
}

REQUIRED_TEST_PACKAGES = {
    "Microsoft.Playwright",
    "NUnit",
    "NUnit3TestAdapter",
    "NUnit.Analyzers",
    "Microsoft.NET.Test.Sdk",
    "FluentAssertions",
    "coverlet.collector",
}

REQUIRED_SHARED_PACKAGES = {
    "Microsoft.Data.SqlClient",
    "FluentAssertions",
}

CENTRAL_VERSIONS = {
    "FluentAssertions": "8.10.0",
    "Microsoft.Data.SqlClient": "7.0.1",
    "Microsoft.NET.Test.Sdk": "17.8.0",
    "Microsoft.Playwright": "1.60.0",
    "NUnit": "3.13.3",
    "NUnit3TestAdapter": "4.2.1",
    "NUnit.Analyzers": "3.6.1",
    "coverlet.collector": "6.0.0",
}

APPSETTINGS_TEST = ROOT / "CVIS.Automation.Tests" / "appsettings.test.json"

DB_CONNECTION = (
    "Server=THOUSANDSUNNY;"
    "Database=EPV_REPORTING;"
    "Trusted_Connection=True;"
    "TrustServerCertificate=True;"
)


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


def csproj_files() -> list[Path]:
    ignored = {".git", ".vs", ".contollo", "bin", "obj", "node_modules", "packages"}
    return sorted(
        path for path in ROOT.rglob("*.csproj")
        if not any(part in ignored for part in path.parts)
    )


def remove_forbidden_package_references(csproj: Path) -> None:
    tree = ET.parse(csproj)
    root = tree.getroot()
    changed = False

    for item_group in list(root.findall("ItemGroup")):
        for package_ref in list(item_group.findall("PackageReference")):
            package = package_ref.attrib.get("Include") or package_ref.attrib.get("Update")
            if package and package in FORBIDDEN_PACKAGES:
                item_group.remove(package_ref)
                changed = True
                print(f"Removed forbidden PackageReference {package} from {csproj.relative_to(ROOT)}")
                continue

            # CPVM: PackageReference must not carry Version.
            if package_ref.attrib.pop("Version", None) is not None:
                changed = True

            version_node = package_ref.find("Version")
            if version_node is not None:
                package_ref.remove(version_node)
                changed = True

        if len(item_group) == 0 and (not item_group.text or not item_group.text.strip()):
            root.remove(item_group)
            changed = True

    if changed:
        indent_xml(root)
        tree.write(csproj, encoding="utf-8", xml_declaration=True)


def has_package(root: ET.Element, package: str) -> bool:
    for package_ref in root.findall(".//PackageReference"):
        name = package_ref.attrib.get("Include") or package_ref.attrib.get("Update")
        if name == package:
            return True
    return False


def ensure_package_references(csproj: Path, packages: set[str]) -> None:
    tree = ET.parse(csproj)
    root = tree.getroot()
    changed = False

    item_group = None
    for candidate in root.findall("ItemGroup"):
        if candidate.findall("PackageReference"):
            item_group = candidate
            break

    if item_group is None:
        item_group = ET.SubElement(root, "ItemGroup")
        changed = True

    for package in sorted(packages):
        if package in FORBIDDEN_PACKAGES:
            continue
        if not has_package(root, package):
            ET.SubElement(item_group, "PackageReference", {"Include": package})
            changed = True
            print(f"Added PackageReference {package} to {csproj.relative_to(ROOT)}")

    if changed:
        indent_xml(root)
        tree.write(csproj, encoding="utf-8", xml_declaration=True)


def ensure_project_reference(csproj: Path, include: str) -> None:
    if not csproj.exists():
        return

    tree = ET.parse(csproj)
    root = tree.getroot()

    for project_ref in root.findall(".//ProjectReference"):
        existing = project_ref.attrib.get("Include", "")
        if existing.lower() == include.lower():
            return

    item_group = None
    for candidate in root.findall("ItemGroup"):
        if candidate.findall("ProjectReference"):
            item_group = candidate
            break

    if item_group is None:
        item_group = ET.SubElement(root, "ItemGroup")

    ET.SubElement(item_group, "ProjectReference", {"Include": include})
    indent_xml(root)
    tree.write(csproj, encoding="utf-8", xml_declaration=True)
    print(f"Added ProjectReference {include} to {csproj.relative_to(ROOT)}")


def update_directory_packages_props() -> None:
    path = ROOT / "Directory.Packages.props"

    if path.exists():
        tree = ET.parse(path)
        root = tree.getroot()
    else:
        root = ET.Element("Project")
        tree = ET.ElementTree(root)

    property_group = root.find("PropertyGroup")
    if property_group is None:
        property_group = ET.SubElement(root, "PropertyGroup")

    manage = property_group.find("ManagePackageVersionsCentrally")
    if manage is None:
        manage = ET.SubElement(property_group, "ManagePackageVersionsCentrally")
    manage.text = "true"

    for item_group in list(root.findall("ItemGroup")):
        for package_version in list(item_group.findall("PackageVersion")):
            package = package_version.attrib.get("Include") or package_version.attrib.get("Update")
            if package in FORBIDDEN_PACKAGES:
                item_group.remove(package_version)
                print(f"Removed forbidden PackageVersion {package} from Directory.Packages.props")

    item_group = None
    for candidate in root.findall("ItemGroup"):
        if candidate.findall("PackageVersion"):
            item_group = candidate
            break
    if item_group is None:
        item_group = ET.SubElement(root, "ItemGroup")

    existing = {
        (node.attrib.get("Include") or node.attrib.get("Update")): node
        for node in item_group.findall("PackageVersion")
    }

    for package, version in sorted(CENTRAL_VERSIONS.items()):
        if package in existing:
            node = existing[package]
            node.set("Version", node.attrib.get("Version") or version)
        else:
            ET.SubElement(item_group, "PackageVersion", {"Include": package, "Version": version})
            print(f"Added PackageVersion {package} to Directory.Packages.props")

    # Remove empty item groups.
    for item_group in list(root.findall("ItemGroup")):
        if len(item_group) == 0:
            root.remove(item_group)

    indent_xml(root)
    tree.write(path, encoding="utf-8", xml_declaration=True)


def patch_projects() -> None:
    for csproj in csproj_files():
        remove_forbidden_package_references(csproj)

    cpn = ROOT / "CVIS.Playwright.NUnitCompat" / "CVIS.Playwright.NUnitCompat.csproj"
    cpn_tests = ROOT / "CVIS.Playwright.NUnitCompat.Tests" / "CVIS.Playwright.NUnitCompat.Tests.csproj"
    automation_tests = ROOT / "CVIS.Automation.Tests" / "CVIS.Automation.Tests.csproj"
    shared = ROOT / "CVIS.Playwright.Automation.Shared" / "CVIS.Playwright.Automation.Shared.csproj"

    if cpn.exists():
        ensure_package_references(cpn, {"Microsoft.Playwright", "NUnit"})

    if cpn_tests.exists():
        ensure_package_references(cpn_tests, REQUIRED_TEST_PACKAGES)
        ensure_project_reference(cpn_tests, r"..\CVIS.Playwright.NUnitCompat\CVIS.Playwright.NUnitCompat.csproj")

    if automation_tests.exists():
        ensure_package_references(automation_tests, REQUIRED_TEST_PACKAGES)
        ensure_project_reference(automation_tests, r"..\CVIS.Playwright.NUnitCompat\CVIS.Playwright.NUnitCompat.csproj")
        if shared.exists():
            ensure_project_reference(automation_tests, r"..\CVIS.Playwright.Automation.Shared\CVIS.Playwright.Automation.Shared.csproj")

    if shared.exists():
        ensure_package_references(shared, REQUIRED_SHARED_PACKAGES)


def patch_csharp_files() -> None:
    ignored = {".git", ".vs", ".contollo", "bin", "obj", "node_modules", "packages"}

    replacements = [
        ("using Microsoft.Playwright.NUnit;", "using CVIS.Playwright.NUnitCompat;"),
        (": PageTest", ": CVISPageTest"),
        (": ContextTest", ": CVISContextTest"),
        (": BrowserTest", ": CVISBrowserTest"),
        (": PlaywrightTest", ": CVISPlaywrightTest"),
        (": APIRequestContextTest", ": CVISApiTest"),
        (": ApiTest", ": CVISApiTest"),
    ]

    for path in ROOT.rglob("*.cs"):
        if any(part in ignored for part in path.parts):
            continue

        text = path.read_text(encoding="utf-8")
        original = text

        for old, new in replacements:
            text = text.replace(old, new)

        # Broader inheritance patterns with generic whitespace/newlines.
        text = re.sub(r":\s*PageTest\b", ": CVISPageTest", text)
        text = re.sub(r":\s*ContextTest\b", ": CVISContextTest", text)
        text = re.sub(r":\s*BrowserTest\b", ": CVISBrowserTest", text)
        text = re.sub(r":\s*PlaywrightTest\b", ": CVISPlaywrightTest", text)

        if "CVIS.Playwright.NUnitCompat" in text and "using CVIS.Playwright.NUnitCompat;" not in text:
            lines = text.splitlines()
            insert_at = 0
            while insert_at < len(lines) and lines[insert_at].startswith("using "):
                insert_at += 1
            lines.insert(insert_at, "using CVIS.Playwright.NUnitCompat;")
            text = "\n".join(lines) + ("\n" if original.endswith("\n") else "")

        if text != original:
            path.write_text(text, encoding="utf-8")
            print(f"Patched CPN usage in {path.relative_to(ROOT)}")


def update_appsettings_test() -> None:
    data = {}

    if APPSETTINGS_TEST.exists():
        try:
            data = json.loads(APPSETTINGS_TEST.read_text(encoding="utf-8-sig"))
        except json.JSONDecodeError:
            backup = APPSETTINGS_TEST.with_suffix(APPSETTINGS_TEST.suffix + ".before-cpn-db-fix")
            backup.write_text(APPSETTINGS_TEST.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
            data = {}

    data.setdefault("ConnectionStrings", {})
    data["ConnectionStrings"]["DefaultConnection"] = DB_CONNECTION

    APPSETTINGS_TEST.parent.mkdir(parents=True, exist_ok=True)
    APPSETTINGS_TEST.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"Updated DB connection string in {APPSETTINGS_TEST.relative_to(ROOT)}")


def write_readme() -> None:
    path = ROOT / "README_CPN_MIGRATION.md"
    path.write_text(
        """# CPN Migration

## Removed / blocked packages

These packages should not be used by CVIS after the CPN migration:

```text
Microsoft.Playwright.NUnit
System.Text.Json explicit PackageReference
xUnit packages
```

## Kept packages

```text
Microsoft.Playwright
NUnit
NUnit3TestAdapter
NUnit.Analyzers
Microsoft.NET.Test.Sdk
FluentAssertions
coverlet.collector
Microsoft.Data.SqlClient
```

## CPN replacement classes

```text
Microsoft.Playwright.NUnit.PlaywrightTest -> CVISPlaywrightTest
Microsoft.Playwright.NUnit.BrowserTest    -> CVISBrowserTest
Microsoft.Playwright.NUnit.ContextTest    -> CVISContextTest
Microsoft.Playwright.NUnit.PageTest       -> CVISPageTest
API helper usage                           -> CVISApiTest
```

## DB configuration

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=THOUSANDSUNNY;Database=EPV_REPORTING;Trusted_Connection=True;TrustServerCertificate=True;"
  }
}
```
""",
        encoding="utf-8")


def main() -> None:
    patch_projects()
    update_directory_packages_props()
    patch_csharp_files()
    update_appsettings_test()
    write_readme()
    print("CPN migration package applied.")
    print("Forbidden NuGet references removed and CPN references added.")


if __name__ == "__main__":
    main()
