using Microsoft.Playwright;
using NUnit.Framework;

namespace CVIS.Playwright.NUnitCompat;

/// <summary>
/// CVIS equivalent of Microsoft.Playwright.NUnit.ContextTest.
/// Creates one BrowserContext per test.
/// </summary>
public class CVISContextTest : CVISBrowserTest
{
    public IBrowserContext Context { get; private set; } = null!;

    [SetUp]
    public async Task CVISContextSetupAsync()
    {
        Context = await NewContext(ContextOptions()).ConfigureAwait(false);
    }

    public virtual BrowserNewContextOptions ContextOptions()
    {
        return new BrowserNewContextOptions
        {
            Locale = "en-US",
            ColorScheme = ColorScheme.Light
        };
    }
}
