using Microsoft.Playwright;
using NUnit.Framework;

namespace CVIS.Playwright.NUnitCompat;

public abstract class CVISPageTest : CVISContextTest
{
    public IPage Page { get; private set; } = null!;

    [SetUp]
    public async Task CVISPageSetupAsync()
    {
        Page = await Context.NewPageAsync().ConfigureAwait(false);
    }
}
