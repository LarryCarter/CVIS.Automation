r"""
CVIS RDEL Update Script
Package: CVIS Organize Shared CPN Projects

Purpose:
    Organize test shared code into proper projects:

    1. CVIS.Playwright.NUnitCompat
       - CPN runtime/base classes.

    2. CVIS.Playwright.NUnitCompat.Tests
       - CPN unit/compatibility tests.

    3. CVIS.Playwright.Automation.Shared
       - Shared automation utilities used by functional test projects:
         Console helpers, DB helpers, config/data loading, reporting.

    4. CVIS.Automation.Tests
       - Functional regression tests only.

This package does not replace PolicyDrift tests yet.
"""

from __future__ import annotations

from pathlib import Path
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET


SOLUTION_ROOT = Path.cwd()

AUTOMATION_TESTS = SOLUTION_ROOT / "CVIS.Automation.Tests"
AUTOMATION_TESTS_CSPROJ = AUTOMATION_TESTS / "CVIS.Automation.Tests.csproj"

SHARED_PROJECT = SOLUTION_ROOT / "CVIS.Playwright.Automation.Shared"
SHARED_PROJECT_CSPROJ = SHARED_PROJECT / "CVIS.Playwright.Automation.Shared.csproj"

CPN_PROJECT = SOLUTION_ROOT / "CVIS.Playwright.NUnitCompat"
CPN_PROJECT_CSPROJ = CPN_PROJECT / "CVIS.Playwright.NUnitCompat.csproj"

CPN_TEST_PROJECT = SOLUTION_ROOT / "CVIS.Playwright.NUnitCompat.Tests"
CPN_TEST_PROJECT_CSPROJ = CPN_TEST_PROJECT / "CVIS.Playwright.NUnitCompat.Tests.csproj"

OLD_SHARED = AUTOMATION_TESTS / "Shared"


MOVE_TO_SHARED_PROJECT = [
    "Console",
    "Database",
    "Helpers",
    "Reporting",
]

REMOVE_FROM_AUTOMATION_TESTS = [
    "PlaywrightCompatTests",
]


def require_layout() -> None:
    if not AUTOMATION_TESTS.exists():
        raise RuntimeError("Cannot find CVIS.Automation.Tests. Run from CVIS.Automation solution root.")

    if not AUTOMATION_TESTS_CSPROJ.exists():
        raise RuntimeError(f"Cannot find {AUTOMATION_TESTS_CSPROJ}")

    SHARED_PROJECT.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_shared_project_file() -> None:
    write_text(
        SHARED_PROJECT_CSPROJ,
        """<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <IsPackable>false</IsPackable>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.Data.SqlClient" Version="7.0.1" />
    <PackageReference Include="FluentAssertions" Version="8.10.0" />
  </ItemGroup>

  <ItemGroup>
    <None Update="**\\TestData\\**\\*.*">
      <CopyToOutputDirectory>PreserveNewest</CopyToOutputDirectory>
    </None>
  </ItemGroup>

</Project>
""",
    )


def move_shared_folders() -> None:
    if not OLD_SHARED.exists():
        return

    for folder_name in MOVE_TO_SHARED_PROJECT:
        source = OLD_SHARED / folder_name
        target = SHARED_PROJECT / folder_name

        if not source.exists():
            continue

        if target.exists():
            shutil.rmtree(target)

        shutil.copytree(source, target)
        shutil.rmtree(source)

        rewrite_namespace_in_folder(
            target,
            "CVIS.Automation.Tests.Shared",
            "CVIS.Playwright.Automation.Shared")


def remove_embedded_cpn_tests_from_automation_tests() -> None:
    if not OLD_SHARED.exists():
        return

    for folder_name in REMOVE_FROM_AUTOMATION_TESTS:
        path = OLD_SHARED / folder_name
        if path.exists():
            shutil.rmtree(path)


def clean_empty_shared_folder() -> None:
    if not OLD_SHARED.exists():
        return

    # Leave Shared folder if it still contains Api/Playwright migration leftovers.
    try:
        if not any(OLD_SHARED.iterdir()):
            OLD_SHARED.rmdir()
    except OSError:
        pass


def rewrite_namespace_in_folder(folder: Path, old: str, new: str) -> None:
    for file in folder.rglob("*.cs"):
        text = file.read_text(encoding="utf-8")
        text = text.replace(old, new)
        file.write_text(text, encoding="utf-8")


def rewrite_project_usings_to_shared_library() -> None:
    for project_folder in [AUTOMATION_TESTS, CPN_TEST_PROJECT]:
        if not project_folder.exists():
            continue

        for file in project_folder.rglob("*.cs"):
            if ".contollo" in file.parts or "bin" in file.parts or "obj" in file.parts:
                continue

            text = file.read_text(encoding="utf-8")
            new_text = text.replace(
                "CVIS.Automation.Tests.Shared.",
                "CVIS.Playwright.Automation.Shared.")

            if new_text != text:
                file.write_text(new_text, encoding="utf-8")


def add_project_reference(csproj: Path, reference: str) -> None:
    if not csproj.exists():
        return

    tree = ET.parse(csproj)
    root = tree.getroot()

    for project_reference in root.findall(".//ProjectReference"):
        if project_reference.attrib.get("Include", "").lower() == reference.lower():
            tree.write(csproj, encoding="utf-8", xml_declaration=True)
            return

    item_group = ET.SubElement(root, "ItemGroup")
    project_reference = ET.SubElement(item_group, "ProjectReference")
    project_reference.set("Include", reference)

    indent_xml(root)
    tree.write(csproj, encoding="utf-8", xml_declaration=True)


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


def add_project_references() -> None:
    add_project_reference(
        AUTOMATION_TESTS_CSPROJ,
        r"..\CVIS.Playwright.Automation.Shared\CVIS.Playwright.Automation.Shared.csproj")

    if CPN_TEST_PROJECT_CSPROJ.exists():
        add_project_reference(
            CPN_TEST_PROJECT_CSPROJ,
            r"..\CVIS.Playwright.Automation.Shared\CVIS.Playwright.Automation.Shared.csproj")


def add_projects_to_solution() -> None:
    sln_files = list(SOLUTION_ROOT.glob("*.sln"))

    if not sln_files:
        return

    sln = sln_files[0]

    for project in [SHARED_PROJECT_CSPROJ, CPN_PROJECT_CSPROJ, CPN_TEST_PROJECT_CSPROJ]:
        if project.exists():
            subprocess.run(
                ["dotnet", "sln", str(sln), "add", str(project)],
                cwd=SOLUTION_ROOT,
                check=False,
                capture_output=True,
                text=True,
            )


def write_architecture_readme() -> None:
    write_text(
        SOLUTION_ROOT / "CVIS_PROJECT_STRUCTURE.md",
        """# CVIS Automation / CPN Project Structure

## CVIS.Playwright.NUnitCompat

CPN runtime compatibility layer.

Contains the replacement classes for the useful parts of `Microsoft.Playwright.NUnit`:

- `CVISWorkerAwareTest`
- `CVISPlaywrightSettingsProvider`
- `CVISPlaywrightTest`
- `CVISBrowserService`
- `CVISBrowserTest`
- `CVISContextTest`
- `CVISPageTest`
- `CVISApiTest`

## CVIS.Playwright.NUnitCompat.Tests

CPN unit/compatibility tests.

This project validates CPN behavior separately from functional automation tests.

## CVIS.Playwright.Automation.Shared

Shared functional automation utilities.

This project owns shared non-CPN helpers:

- Console app execution helpers
- Database helpers
- Config/data loading helpers
- Regression report helpers

## CVIS.Automation.Tests

Functional regression test project.

This project should contain project-specific automation suites such as:

- PolicyDrift
- Unity
- LegacySustainment

It should not contain CPN compatibility tests.
""",
    )


def main() -> None:
    require_layout()
    write_shared_project_file()
    move_shared_folders()
    remove_embedded_cpn_tests_from_automation_tests()
    rewrite_project_usings_to_shared_library()
    add_project_references()
    add_projects_to_solution()
    clean_empty_shared_folder()
    write_architecture_readme()

    print("Organized shared code into CVIS.Playwright.Automation.Shared / CPN / CPN.Tests.")
    print("PolicyDrift behavior was not replaced.")


if __name__ == "__main__":
    main()
