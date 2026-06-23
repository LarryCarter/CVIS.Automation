r"""
CVIS RDEL Update Script
Package: CVIS Fix NU1008 Central Package Versions

Purpose:
    Fix NU1008 errors by moving package versions out of PackageReference
    entries and into Directory.Packages.props as PackageVersion entries.

Runs from solution root:
    C:\Users\larry\source\repos\CVIS.Automation
"""

from __future__ import annotations

from pathlib import Path
import xml.etree.ElementTree as ET


SOLUTION_ROOT = Path.cwd()
DIRECTORY_PACKAGES_PROPS = SOLUTION_ROOT / "Directory.Packages.props"


DEFAULT_PACKAGE_VERSIONS = {
    "FluentAssertions": "8.10.0",
    "Microsoft.Data.SqlClient": "7.0.1",
    "Microsoft.NET.Test.Sdk": "17.8.0",
    "Microsoft.Playwright": "1.60.0",
    "Microsoft.Playwright.NUnit": "1.60.0",
    "NUnit": "3.13.3",
    "NUnit3TestAdapter": "4.2.1",
    "NUnit.Analyzers": "3.6.1",
    "coverlet.collector": "6.0.0",
    "System.Text.Json": "10.0.8",
}


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


def find_csproj_files() -> list[Path]:
    ignored_parts = {
        ".git",
        ".vs",
        ".contollo",
        "bin",
        "obj",
        "packages",
        "node_modules",
    }

    results: list[Path] = []

    for path in SOLUTION_ROOT.rglob("*.csproj"):
        if any(part in ignored_parts for part in path.parts):
            continue

        results.append(path)

    return sorted(results)


def remove_versions_from_package_references() -> dict[str, str]:
    discovered_versions: dict[str, str] = {}

    for csproj in find_csproj_files():
        tree = ET.parse(csproj)
        root = tree.getroot()
        changed = False

        for package_reference in root.findall(".//PackageReference"):
            package_name = (
                package_reference.attrib.get("Include")
                or package_reference.attrib.get("Update")
            )

            if not package_name:
                continue

            version = package_reference.attrib.pop("Version", None)

            version_child = package_reference.find("Version")
            if version_child is not None:
                if not version:
                    version = (version_child.text or "").strip() or None

                package_reference.remove(version_child)
                changed = True

            if version:
                discovered_versions.setdefault(package_name, version)
                changed = True

        if changed:
            indent_xml(root)
            tree.write(csproj, encoding="utf-8", xml_declaration=True)
            print(f"Updated PackageReference versions in {csproj.relative_to(SOLUTION_ROOT)}")

    return discovered_versions


def ensure_directory_packages_props(discovered_versions: dict[str, str]) -> None:
    versions = dict(DEFAULT_PACKAGE_VERSIONS)
    versions.update(discovered_versions)

    if DIRECTORY_PACKAGES_PROPS.exists():
        tree = ET.parse(DIRECTORY_PACKAGES_PROPS)
        root = tree.getroot()
    else:
        root = ET.Element("Project")
        tree = ET.ElementTree(root)

    property_group = None
    for item in root.findall("PropertyGroup"):
        property_group = item
        break

    if property_group is None:
        property_group = ET.SubElement(root, "PropertyGroup")

    manage = property_group.find("ManagePackageVersionsCentrally")
    if manage is None:
        manage = ET.SubElement(property_group, "ManagePackageVersionsCentrally")

    manage.text = "true"

    central_item_group = None
    for item_group in root.findall("ItemGroup"):
        if item_group.findall("PackageVersion"):
            central_item_group = item_group
            break

    if central_item_group is None:
        central_item_group = ET.SubElement(root, "ItemGroup")

    existing = {}
    for package_version in central_item_group.findall("PackageVersion"):
        package_name = (
            package_version.attrib.get("Include")
            or package_version.attrib.get("Update")
        )

        if package_name:
            existing[package_name] = package_version

    for package_name in sorted(versions.keys(), key=str.lower):
        version = versions[package_name]

        if package_name in existing:
            package_version = existing[package_name]

            if "Version" not in package_version.attrib and not (package_version.text or "").strip():
                package_version.set("Version", version)
        else:
            package_version = ET.SubElement(central_item_group, "PackageVersion")
            package_version.set("Include", package_name)
            package_version.set("Version", version)

    indent_xml(root)
    tree.write(DIRECTORY_PACKAGES_PROPS, encoding="utf-8", xml_declaration=True)
    print(f"Updated {DIRECTORY_PACKAGES_PROPS.relative_to(SOLUTION_ROOT)}")


def main() -> None:
    discovered_versions = remove_versions_from_package_references()
    ensure_directory_packages_props(discovered_versions)

    print("NU1008 central package version fix complete.")
    print("PackageReference items no longer define versions.")
    print("PackageVersion items are centralized in Directory.Packages.props.")


if __name__ == "__main__":
    main()
