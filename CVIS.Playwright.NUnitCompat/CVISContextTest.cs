using Microsoft.Playwright;
using NUnit.Framework;

namespace CVIS.Playwright.NUnitCompat;

public abstract class CVISContextTest : CVISBrowserTest
{
    public IBrowserContext Context { get; private set; } = null!;

    [SetUp]
    public async Task CVISContextSetupAsync()
    {
        Context = await NewContext(ContextOptions()).ConfigureAwait(false);
    }

    public virtual BrowserNewContextOptions ContextOptions() => new() { Locale = "en-US", ColorScheme = ColorScheme.Light };
}
