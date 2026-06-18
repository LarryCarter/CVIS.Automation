r"""
CVIS RDEL Update Script
Package: CVIS Fix API Test Compatibility

Purpose:
    Adds missing CVISApiTest compatibility members expected by tests:
    - ApiContext property
    - NewApiRequestContextAsync(...)
    - NewApiContextAsync(...)
"""

from __future__ import annotations

from pathlib import Path


SOLUTION_ROOT = Path.cwd()
COMPAT_ROOT = SOLUTION_ROOT / "CVIS.Playwright.NUnitCompat"
TARGET_FILE = COMPAT_ROOT / "CVISApiTest.cs"


def require_layout() -> None:
    if not COMPAT_ROOT.exists():
        raise RuntimeError("Cannot find CVIS.Playwright.NUnitCompat. Run the feature layer package first.")

    COMPAT_ROOT.mkdir(parents=True, exist_ok=True)


def write_api_test() -> None:
    TARGET_FILE.write_text(
        """using Microsoft.Playwright;
using NUnit.Framework;

namespace CVIS.Playwright.NUnitCompat;

/// <summary>
/// CVIS API-focused extension for console/API/database regression projects.
/// Provides APIRequestContext creation without requiring browser/page setup.
/// </summary>
public class CVISApiTest : CVISPlaywrightTest
{
    private readonly List<IAPIRequestContext> _apiContexts = new();

    public IAPIRequestContext ApiContext { get; private set; } = null!;

    [SetUp]
    public async Task CVISApiSetupAsync()
    {
        ApiContext = await NewApiRequestContextAsync();
    }

    [TearDown]
    public async Task CVISApiTearDownAsync()
    {
        foreach (var context in _apiContexts)
        {
            await context.DisposeAsync().ConfigureAwait(false);
        }

        _apiContexts.Clear();
        ApiContext = null!;
    }

    public Task<IAPIRequestContext> NewApiRequestContextAsync(
        string? baseUrl = null,
        IDictionary<string, string>? headers = null,
        bool ignoreHttpsErrors = true)
    {
        return NewApiContextAsync(baseUrl, headers, ignoreHttpsErrors);
    }

    public async Task<IAPIRequestContext> NewApiContextAsync(
        string? baseUrl = null,
        IDictionary<string, string>? headers = null,
        bool ignoreHttpsErrors = true)
    {
        var context = await Playwright.APIRequest.NewContextAsync(
            new APIRequestNewContextOptions
            {
                BaseURL = baseUrl,
                ExtraHTTPHeaders = headers,
                IgnoreHTTPSErrors = ignoreHttpsErrors
            }).ConfigureAwait(false);

        _apiContexts.Add(context);
        return context;
    }
}
""",
        encoding="utf-8",
    )


def main() -> None:
    require_layout()
    write_api_test()
    print(f"Fixed {TARGET_FILE}")


if __name__ == "__main__":
    main()
