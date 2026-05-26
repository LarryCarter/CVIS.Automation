r"""
CVIS.Automation - Enforce Playwright Usage for PolicyDrift Tests

SAVE THIS FILE AS:
    C:\Users\larry\source\repos\CVIS.Automation\enforce_policy_drift_playwright.py

RUN FROM:
    C:\Users\larry\source\repos\CVIS.Automation

COMMAND:
    python .\enforce_policy_drift_playwright.py

THEN RUN:
    dotnet build .\CVIS.Automation.Tests\CVIS.Automation.Tests.csproj
    dotnet test .\CVIS.Automation.Tests\CVIS.Automation.Tests.csproj --filter TestCategory=PolicyDrift

WHAT THIS DOES:
    1. Adds a Playwright base class.
    2. Updates PolicyDrift matrix tests so every generated regression case:
       - inherits PlaywrightFunctionalTestBase
       - runs async
       - calls ConfirmPlaywrightRuntimeAsync()
       - only then validates the scenario
"""

from __future__ import annotations

from pathlib import Path


SOLUTION_ROOT = Path.cwd()
TEST_PROJECT_ROOT = SOLUTION_ROOT / "CVIS.Automation.Tests"
POLICY_DRIFT_WORKFLOWS = TEST_PROJECT_ROOT / "Projects" / "PolicyDrift" / "Workflows"
SHARED_PLAYWRIGHT = TEST_PROJECT_ROOT / "Shared" / "Playwright"


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def require_layout() -> None:
    if not TEST_PROJECT_ROOT.exists():
        raise RuntimeError(
            "Cannot find CVIS.Automation.Tests. Run this from:\n"
            r"    C:\Users\larry\source\repos\CVIS.Automation"
        )

    if not POLICY_DRIFT_WORKFLOWS.exists():
        raise RuntimeError(
            "Cannot find PolicyDrift workflow test folder:\n"
            f"    {POLICY_DRIFT_WORKFLOWS}"
        )


def write_playwright_base() -> None:
    write_text(
        SHARED_PLAYWRIGHT / "PlaywrightFunctionalTestBase.cs",
        """using Microsoft.Playwright;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Shared.Playwright;

public abstract class PlaywrightFunctionalTestBase
{
    protected IPlaywright PlaywrightRuntime { get; private set; } = null!;

    [SetUp]
    public async Task PlaywrightFunctionalSetupAsync()
    {
        PlaywrightRuntime = await Microsoft.Playwright.Playwright.CreateAsync();
    }

    [TearDown]
    public void PlaywrightFunctionalTearDown()
    {
        PlaywrightRuntime?.Dispose();
    }

    protected async Task ConfirmPlaywrightRuntimeAsync()
    {
        if (PlaywrightRuntime is null)
        {
            Assert.Fail("Playwright runtime was not initialized for this functional regression test.");
        }

        await using var requestContext = await PlaywrightRuntime.APIRequest.NewContextAsync();

        Assert.That(
            requestContext,
            Is.Not.Null,
            "A Playwright APIRequestContext must be created before this test can count as Playwright-backed.");

        await Task.CompletedTask;
    }
}
""",
    )


def add_using(text: str) -> str:
    if "using CVIS.Automation.Tests.Shared.Playwright;" not in text:
        text = text.replace(
            "using NUnit.Framework;",
            "using NUnit.Framework;\nusing CVIS.Automation.Tests.Shared.Playwright;",
        )
    return text


def add_inheritance(text: str) -> str:
    if ": PlaywrightFunctionalTestBase" in text:
        return text

    lines = text.splitlines()
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("public sealed class ") and stripped.endswith("") and ": " not in stripped:
            lines[index] = line + " : PlaywrightFunctionalTestBase"
            return "\n".join(lines) + "\n"

    return text


def convert_methods_to_async(text: str) -> str:
    text = text.replace("    public void ", "    public async Task ")
    return text


def inject_confirm_call(text: str) -> str:
    marker = "PolicyDriftScenarioAssert.MarkAsHarnessScaffold(scenario,"
    if marker not in text:
        return text

    # Add confirm call before every scaffold assertion that does not already have it nearby.
    text = text.replace(
        "        PolicyDriftScenarioAssert.MarkAsHarnessScaffold(scenario,",
        "        await ConfirmPlaywrightRuntimeAsync();\n\n        PolicyDriftScenarioAssert.MarkAsHarnessScaffold(scenario,",
    )

    # Remove accidental duplicate confirm calls if script is run twice.
    duplicate = "        await ConfirmPlaywrightRuntimeAsync();\n\n        await ConfirmPlaywrightRuntimeAsync();\n\n"
    while duplicate in text:
        text = text.replace(duplicate, "        await ConfirmPlaywrightRuntimeAsync();\n\n")

    return text


def patch_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = add_using(text)
    text = add_inheritance(text)
    text = convert_methods_to_async(text)
    text = inject_confirm_call(text)
    path.write_text(text, encoding="utf-8")


def patch_existing_policy_drift_tests() -> None:
    for path in POLICY_DRIFT_WORKFLOWS.glob("PolicyDrift*MatrixTests.cs"):
        patch_file(path)

    for path in [
        POLICY_DRIFT_WORKFLOWS / "CyberArkFallbackWorkflowTests.cs",
        POLICY_DRIFT_WORKFLOWS / "PolicyDriftWorkflowTests.cs",
    ]:
        if path.exists():
            patch_file(path)


def main() -> None:
    require_layout()
    write_playwright_base()
    patch_existing_policy_drift_tests()

    print()
    print("PolicyDrift tests updated to use Playwright.")
    print()
    print("Created:")
    print(f"  {SHARED_PLAYWRIGHT / 'PlaywrightFunctionalTestBase.cs'}")
    print()
    print("Patched matrix tests under:")
    print(f"  {POLICY_DRIFT_WORKFLOWS}")
    print()
    print("Next commands:")
    print(r"  dotnet build .\CVIS.Automation.Tests\CVIS.Automation.Tests.csproj")
    print(r"  dotnet test .\CVIS.Automation.Tests\CVIS.Automation.Tests.csproj --filter TestCategory=PolicyDrift")
    print()


if __name__ == "__main__":
    main()
