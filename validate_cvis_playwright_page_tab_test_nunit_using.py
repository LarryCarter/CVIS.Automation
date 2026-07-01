from pathlib import Path

TARGET = Path("CVIS.Playwright.NUnitCompat/Base/BaseAutomationCvisPlaywrightPageTabTest.cs")


def main() -> None:
    if not TARGET.exists():
        raise SystemExit(f"Missing expected target file: {TARGET}")

    content = TARGET.read_text(encoding="utf-8-sig")

    required = [
        "using Microsoft.Playwright;",
        "using NUnit.Framework;",
        "public abstract class BaseAutomationCvisPlaywrightPageTabTest : BaseAutomationCvisPlaywrightBrowserTest",
        "TestContext.CurrentContext.Test.FullName",
    ]

    missing = [item for item in required if item not in content]
    if missing:
        raise SystemExit("Validation failed. Missing: " + ", ".join(missing))

    if content.find("using NUnit.Framework;") > content.find("namespace CVIS.Playwright.NUnitCompat.Base;"):
        raise SystemExit("Validation failed. NUnit using appears after namespace declaration.")

    pairs = [("{", "}"), ("(", ")"), ("[", "]")]
    for left, right in pairs:
        if content.count(left) != content.count(right):
            raise SystemExit(f"Validation failed. Unbalanced {left}{right} characters in {TARGET}.")

    print("Validation passed: BaseAutomationCvisPlaywrightPageTabTest imports NUnit.Framework and TestContext resolves.")


if __name__ == "__main__":
    main()
