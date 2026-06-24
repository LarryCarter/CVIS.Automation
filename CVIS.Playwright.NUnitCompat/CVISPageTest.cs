using Microsoft.Playwright;
using NUnit.Framework;
using CVIS.Playwright.NUnitCompat;

namespace CVIS.Playwright.NUnitCompat;

/// <summary>
/// CVIS equivalent of Microsoft.Playwright.NUnit.PageTest.
/// Creates one Page per test.
/// </summary>
public class CVISPageTest : CVISContextTest
{
    public IPage Page { get; private set; } = null!;

    [SetUp]
    public async Task CVISPageSetupAsync()
    {
        Page = await Context.NewPageAsync().ConfigureAwait(false);
    }
}
