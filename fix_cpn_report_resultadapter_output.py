r"""
CVIS RDEL Update Script
Package: CPN Fix ResultAdapter Output

Purpose:
    Fixes CS1061:
        TestContext.ResultAdapter does not contain a definition for Output
"""

from pathlib import Path

ROOT = Path.cwd()
TARGET = ROOT / "CVIS.Playwright.NUnitCompat" / "Reporting" / "CPNReportManager.cs"

def main():
    if not TARGET.exists():
        raise RuntimeError(f"Cannot find {TARGET}")

    text = TARGET.read_text(encoding="utf-8")

    text = text.replace(
        "OutputLines = SplitLines(result.Output),",
        "OutputLines = Array.Empty<string>(),")
    text = text.replace(
        "OutputLines = GetOutputLines(result.Output),",
        "OutputLines = Array.Empty<string>(),")

    text = remove_method(text, "SplitLines")
    text = remove_method(text, "GetOutputLines")

    TARGET.write_text(text, encoding="utf-8")
    print("Fixed invalid ResultAdapter.Output usage in CPNReportManager.cs")


def remove_method(text: str, method_name: str) -> str:
    marker = f"private static IReadOnlyList<string> {method_name}("
    start = text.find(marker)
    if start < 0:
        return text

    brace = text.find("{", start)
    if brace < 0:
        return text

    depth = 0
    end = brace
    while end < len(text):
        char = text[end]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                end += 1
                break
        end += 1

    return text[:start].rstrip() + "\n\n" + text[end:].lstrip()


if __name__ == "__main__":
    main()
