from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
import re


ROOT = Path.cwd()

EXCLUDED_DIRS = {
    ".git",
    ".vs",
    ".contollo",
    "bin",
    "obj",
    "__pycache__",
    "TestResults",
}

METHOD_PATTERN = re.compile(
    r"(?P<attrs>(?:^[ \t]*\[[^\r\n]*\][ \t]*(?:\r?\n))+)"
    r"(?P<sig>^[ \t]*(?:public|private|protected|internal)\s+"
    r"(?:static\s+)?(?:async\s+)?"
    r"(?:void|Task|Task<[^>]+>|ValueTask|ValueTask<[^>]+>)\s+"
    r"(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*"
    r"\([^)]*\)\s*(?:\r?\n)?[ \t]*\{)",
    re.MULTILINE,
)

TRAIT_PATTERN = re.compile(
    r'^[ \t]*\[Trait\(\s*"(?P<key>[^"]+)"\s*,\s*"(?P<value>[^"]+)"\s*\)\][ \t]*(?:\r?\n)?',
    re.MULTILINE,
)


@dataclass
class MethodInfo:
    start: int
    open_brace: int
    close_brace: int
    attrs: str
    signature: str
    name: str
    trait_key: str | None
    trait_value: str | None


def should_skip(path: Path) -> bool:
    return any(part in EXCLUDED_DIRS for part in path.parts)


def iter_csharp_files():
    for path in ROOT.rglob("*.cs"):
        if should_skip(path):
            continue
        yield path


def find_matching_brace(text: str, open_brace_index: int) -> int:
    depth = 0
    in_string = False
    in_char = False
    in_verbatim_string = False
    in_single_line_comment = False
    in_multi_line_comment = False
    i = open_brace_index

    while i < len(text):
        current = text[i]
        nxt = text[i + 1] if i + 1 < len(text) else ""

        if in_single_line_comment:
            if current == "\n":
                in_single_line_comment = False
            i += 1
            continue

        if in_multi_line_comment:
            if current == "*" and nxt == "/":
                in_multi_line_comment = False
                i += 2
                continue
            i += 1
            continue

        if in_string:
            if in_verbatim_string:
                if current == '"' and nxt == '"':
                    i += 2
                    continue
                if current == '"':
                    in_string = False
                    in_verbatim_string = False
                i += 1
                continue

            if current == "\\":
                i += 2
                continue
            if current == '"':
                in_string = False
            i += 1
            continue

        if in_char:
            if current == "\\":
                i += 2
                continue
            if current == "'":
                in_char = False
            i += 1
            continue

        if current == "/" and nxt == "/":
            in_single_line_comment = True
            i += 2
            continue

        if current == "/" and nxt == "*":
            in_multi_line_comment = True
            i += 2
            continue

        if current == "@" and nxt == '"':
            in_string = True
            in_verbatim_string = True
            i += 2
            continue

        if current == '"':
            in_string = True
            i += 1
            continue

        if current == "'":
            in_char = True
            i += 1
            continue

        if current == "{":
            depth += 1

        if current == "}":
            depth -= 1
            if depth == 0:
                return i

        i += 1

    raise ValueError("Could not find matching brace.")


def sanitize_token(value: str) -> str:
    parts = re.split(r"[^A-Za-z0-9]+", value)
    return "".join(part[:1].upper() + part[1:] for part in parts if part) or "Trait"


def method_trait_token(trait_key: str | None, trait_value: str | None) -> str:
    if trait_key and trait_key.lower() == "category" and trait_value:
        return sanitize_token(trait_value)

    if trait_key and trait_value and trait_value.lower() not in {"true", "yes", "1"}:
        return sanitize_token(trait_value)

    if trait_key:
        return sanitize_token(trait_key)

    return "Trait"


def desired_method_name(current_name: str, trait_key: str | None, trait_value: str | None) -> str:
    token = method_trait_token(trait_key, trait_value)

    # Repair prior broken names from sequence 008.
    repaired = current_name.replace("_Category_", f"_{token}_")
    if repaired.endswith("_Category"):
        repaired = repaired[: -len("_Category")] + f"_{token}"

    if repaired != current_name:
        return repaired

    if f"_{token}_" in current_name or current_name.endswith(f"_{token}"):
        return current_name

    for marker in ("_Should", "_When", "_Returns", "_Can", "_Has", "_Is"):
        if marker in current_name:
            return current_name.replace(marker, f"_{token}{marker}", 1)

    return f"{current_name}_{token}"


def read_methods(text: str) -> list[MethodInfo]:
    methods: list[MethodInfo] = []

    for match in METHOD_PATTERN.finditer(text):
        attrs = match.group("attrs")
        name = match.group("name")
        open_brace = text.find("{", match.start("sig"))

        if open_brace < 0:
            continue

        try:
            close_brace = find_matching_brace(text, open_brace)
        except ValueError:
            continue

        traits = list(TRAIT_PATTERN.finditer(attrs))
        trait_key = traits[0].group("key") if len(traits) == 1 else None
        trait_value = traits[0].group("value") if len(traits) == 1 else None

        methods.append(MethodInfo(
            start=match.start(),
            open_brace=open_brace,
            close_brace=close_brace,
            attrs=attrs,
            signature=match.group("sig"),
            name=name,
            trait_key=trait_key,
            trait_value=trait_value,
        ))

    return methods


def replace_method_name_once(method_text: str, old_name: str, new_name: str) -> str:
    return re.sub(
        rf"\b{re.escape(old_name)}\s*\(",
        f"{new_name}(",
        method_text,
        count=1,
    )


def process_file(path: Path) -> list[str]:
    original = path.read_text(encoding="utf-8-sig")
    methods = read_methods(original)
    by_name = defaultdict(list)

    for method in methods:
        by_name[method.name].append(method)

    replacements: list[tuple[int, int, str]] = []
    changed_names: list[str] = []
    used_names = {method.name for method in methods}

    for name, group in by_name.items():
        if len(group) <= 1:
            continue

        for index, method in enumerate(group):
            desired = desired_method_name(method.name, method.trait_key, method.trait_value)

            if desired == method.name:
                token = method_trait_token(method.trait_key, method.trait_value)
                desired = f"{method.name}_{token}"

            unique = desired
            counter = 2

            while unique in used_names and unique != method.name:
                unique = f"{desired}_{counter}"
                counter += 1

            if unique == method.name:
                continue

            used_names.add(unique)

            method_text = original[method.start:method.close_brace + 1]
            updated_method_text = replace_method_name_once(method_text, method.name, unique)

            replacements.append((method.start, method.close_brace + 1, updated_method_text))
            changed_names.append(f"{method.name} -> {unique}")

    if not replacements:
        return []

    updated = original

    for start, end, replacement in sorted(replacements, key=lambda item: item[0], reverse=True):
        updated = updated[:start] + replacement + updated[end:]

    path.write_text(updated, encoding="utf-8")
    return changed_names


def append_section(path: Path, title: str, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8") if path.exists() else ""

    if title in existing:
        return

    content = existing.rstrip() + "\n\n" if existing.strip() else ""
    content += f"{title}\n\n{body.strip()}\n"
    path.write_text(content, encoding="utf-8")


def update_docs() -> None:
    append_section(
        ROOT / "docs" / "DECISIONS.md",
        "## 2026-07-01 — xUnit Category Trait Names Use Trait Value",
        """
Decision: when duplicating xUnit tests for category-counting compatibility, method names must use the trait value when the trait key is `Category`.

Correct:

```csharp
[Trait("Category", "PolicyDrift")]
public void Example_PolicyDrift_ShouldPass()

[Trait("Category", "ConsoleRegression")]
public void Example_ConsoleRegression_ShouldPass()
```

Incorrect:

```csharp
public void Example_Category_ShouldPass()
public void Example_Category_ShouldPass()
```

Reason: multiple traits commonly share the key `Category`, so using the key creates duplicate method names and causes CS0111/xUnit1024.
""",
    )

    append_section(
        ROOT / "docs" / "AI_INSTRUCTIONS.md",
        "## xUnit Category Trait Naming Rule",
        """
When generating duplicated xUnit test methods for countable traits:

- If the trait key is `Category`, use the trait value in the method name.
- If the trait key is not `Category`, use the trait value when meaningful, otherwise use the trait key.
- Never generate multiple methods named `*_Category_*` for different category values.
""",
    )

    append_section(
        ROOT / "docs" / "memory.md",
        "## xUnit category trait method names",
        """
RDEL sequence 009 fixed sequence 008 duplicate method names.

Rule: for `[Trait("Category", "...")]`, method names must include the category value, not the literal word `Category`.
""",
    )

    append_section(
        ROOT / "docs" / "context.md",
        "## xUnit trait method-name repair",
        """
When xUnit category traits are duplicated into physical methods, the method name uses the trait value.

Example: `[Trait("Category", "PolicyDrift")]` becomes `_PolicyDrift_`, not `_Category_`.
""",
    )


def main() -> None:
    changed: dict[str, list[str]] = {}

    for path in iter_csharp_files():
        changes = process_file(path)
        if changes:
            changed[str(path.relative_to(ROOT))] = changes

    report = ROOT / "docs" / "xunit-trait-duplicate-name-repair-report.md"
    report.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# xUnit Trait Duplicate Name Repair Report",
        "",
        "This report was generated by RDEL package 009.",
        "",
        "Purpose: repair duplicate method names created when RDEL package 008 used trait key instead of trait value for `[Trait(\"Category\", ...)]` methods.",
        "",
    ]

    if not changed:
        lines.append("No duplicate method names requiring repair were found.")
    else:
        for file, changes in changed.items():
            lines.append(f"## `{file}`")
            lines.append("")
            for change in changes:
                lines.append(f"- `{change}`")
            lines.append("")

    report.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

    update_docs()

    print(f"xUnit duplicate method-name repair complete. Changed files: {len(changed)}")
    print("Report: docs/xunit-trait-duplicate-name-repair-report.md")


if __name__ == "__main__":
    main()
