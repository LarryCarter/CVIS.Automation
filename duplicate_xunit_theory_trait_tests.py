from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Iterable


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

THEORY_PATTERN = re.compile(
    r'^[ \t]*\[Theory(?:\([^\)]*\))?\][ \t]*(?:\r?\n)?',
    re.MULTILINE,
)


@dataclass(frozen=True)
class Trait:
    key: str
    value: str


@dataclass(frozen=True)
class Change:
    path: Path
    method_name: str
    trait_pairs: list[str]
    generated_methods: list[str]


def should_skip(path: Path) -> bool:
    return any(part in EXCLUDED_DIRS for part in path.parts)


def iter_csharp_files() -> Iterable[Path]:
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


def method_trait_token(trait: Trait) -> str:
    if trait.key.lower() == "category":
        return sanitize_token(trait.value)

    if trait.value.lower() not in {"true", "yes", "1"}:
        return sanitize_token(trait.value)

    return sanitize_token(trait.key)


def trait_method_name(original_name: str, trait: Trait) -> str:
    token = method_trait_token(trait)

    repaired = original_name.replace("_Category_", f"_{token}_")
    if repaired.endswith("_Category"):
        repaired = repaired[: -len("_Category")] + f"_{token}"

    if repaired != original_name:
        return repaired

    if f"_{token}_" in original_name or original_name.endswith(f"_{token}"):
        return original_name

    for marker in ("_Should", "_When", "_Returns", "_Can", "_Has", "_Is", "_Produces", "_Validates"):
        if marker in original_name:
            return original_name.replace(marker, f"_{token}{marker}", 1)

    return f"{original_name}_{token}"


def build_attribute_block(attrs: str, trait: Trait) -> str:
    attrs_without_traits = TRAIT_PATTERN.sub("", attrs)

    if not THEORY_PATTERN.search(attrs_without_traits):
        return attrs_without_traits

    return attrs_without_traits + f'[Trait("{trait.key}", "{trait.value}")]\n'


def unique_method_name(base_name: str, used_names: set[str]) -> str:
    if base_name not in used_names:
        used_names.add(base_name)
        return base_name

    counter = 2
    while f"{base_name}_{counter}" in used_names:
        counter += 1

    unique = f"{base_name}_{counter}"
    used_names.add(unique)
    return unique


def process_file(path: Path) -> Change | None:
    original = path.read_text(encoding="utf-8-sig")
    used_names = set(re.findall(r"\b(?:public|private|protected|internal)\s+(?:static\s+)?(?:async\s+)?(?:void|Task|Task<[^>]+>|ValueTask|ValueTask<[^>]+>)\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", original))
    replacements: list[tuple[int, int, str, Change]] = []

    for match in METHOD_PATTERN.finditer(original):
        attrs = match.group("attrs")
        method_name = match.group("name")

        if not THEORY_PATTERN.search(attrs):
            continue

        traits = [
            Trait(key=item.group("key"), value=item.group("value"))
            for item in TRAIT_PATTERN.finditer(attrs)
        ]

        if len(traits) <= 1:
            continue

        open_brace_index = original.find("{", match.start("sig"))
        if open_brace_index < 0:
            continue

        try:
            close_brace_index = find_matching_brace(original, open_brace_index)
        except ValueError:
            continue

        method_core = original[match.start("sig"):close_brace_index + 1]
        generated_blocks: list[str] = []
        generated_names: list[str] = []

        for trait in traits:
            base_new_name = trait_method_name(method_name, trait)
            new_name = unique_method_name(base_new_name, used_names)

            new_attrs = build_attribute_block(attrs, trait)
            new_method_core = re.sub(
                rf"\b{re.escape(method_name)}\s*\(",
                f"{new_name}(",
                method_core,
                count=1,
            )

            generated_blocks.append(new_attrs + new_method_core)
            generated_names.append(new_name)

        replacement = "\n\n".join(generated_blocks)
        change = Change(
            path=path,
            method_name=method_name,
            trait_pairs=[f'{trait.key}={trait.value}' for trait in traits],
            generated_methods=generated_names,
        )
        replacements.append((match.start(), close_brace_index + 1, replacement, change))

    if not replacements:
        return None

    updated = original

    for start, end, replacement, _ in reversed(replacements):
        updated = updated[:start] + replacement + updated[end:]

    path.write_text(updated, encoding="utf-8")

    return Change(
        path=path,
        method_name=", ".join(change.method_name for *_, change in replacements),
        trait_pairs=[pair for *_, change in replacements for pair in change.trait_pairs],
        generated_methods=[method for *_, change in replacements for method in change.generated_methods],
    )


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
        "## 2026-07-01 — xUnit Theory Trait Counting Compatibility",
        """
Decision: xUnit `[Theory]` methods follow the same external counting rule as `[Fact]` methods.

If a theory needs to count under more than one trait category, it must be represented as one physical theory method per trait. Each generated method keeps the same theory data attributes, such as `[InlineData]`, `[MemberData]`, or `[ClassData]`, and receives exactly one countable `[Trait]`.

When the trait key is `Category`, method names must use the trait value.

Correct:

```csharp
[Theory]
[InlineData("a")]
[Trait("Category", "PolicyDrift")]
public void Example_PolicyDrift_ShouldPass(string value)

[Theory]
[InlineData("a")]
[Trait("Category", "ConsoleRegression")]
public void Example_ConsoleRegression_ShouldPass(string value)
```
""",
    )

    append_section(
        ROOT / "docs" / "AI_INSTRUCTIONS.md",
        "## xUnit Theory Trait Counting Rule",
        """
When generating xUnit `[Theory]` tests for this repository, do not put multiple category-counting `[Trait]` attributes on the same method.

If a theory must count for multiple categories, generate one physical theory method per trait. Preserve all data attributes (`[InlineData]`, `[MemberData]`, `[ClassData]`) on each duplicated theory method.

If the trait key is `Category`, use the trait value in the method name.
""",
    )

    append_section(
        ROOT / "docs" / "memory.md",
        "## xUnit theory trait duplication",
        """
RDEL sequence 010 extends the sequence 008/009 xUnit trait-counting compatibility to `[Theory]` methods.

Rule: one physical theory method per countable trait, preserving theory data attributes.
""",
    )

    append_section(
        ROOT / "docs" / "context.md",
        "## xUnit theory trait method duplication",
        """
For xUnit `[Theory]` tests, multiple category traits on one method are not reliable for the external counting tool.

The repository uses one physical `[Theory]` method per countable trait when categories must be counted separately. All theory data attributes are preserved on each duplicate.
""",
    )


def write_report(changes: list[Change]) -> None:
    report = ROOT / "docs" / "xunit-theory-trait-method-duplication-report.md"
    report.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# xUnit Theory Trait Method Duplication Report",
        "",
        "This report was generated by RDEL package 010.",
        "",
        "Purpose: split xUnit `[Theory]` methods with multiple `[Trait]` attributes into separate physical theory methods so external test-count tools can count each category.",
        "",
    ]

    if not changes:
        lines.append("No multi-trait xUnit `[Theory]` methods were found.")
    else:
        lines.append("## Changed files")
        lines.append("")

        for change in changes:
            rel = change.path.relative_to(ROOT)
            lines.append(f"### `{rel}`")
            lines.append("")
            lines.append(f"- Original method(s): `{change.method_name}`")
            lines.append(f"- Trait pairs: {', '.join(f'`{pair}`' for pair in change.trait_pairs)}")
            lines.append("- Generated methods:")
            for method in change.generated_methods:
                lines.append(f"  - `{method}`")
            lines.append("")

    report.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    changes: list[Change] = []

    for path in iter_csharp_files():
        change = process_file(path)
        if change is not None:
            changes.append(change)

    write_report(changes)
    update_docs()

    print(f"xUnit theory trait method duplication complete. Changed files: {len(changes)}")
    print("Report: docs/xunit-theory-trait-method-duplication-report.md")


if __name__ == "__main__":
    main()
