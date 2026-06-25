using Microsoft.Playwright;
using NUnit.Framework;

namespace CVIS.Playwright.NUnitCompat.Base;

/// <summary>
/// Browser lane base class with a fresh browser context and page for each test.
/// </summary>
[TestFixture]
public abstract class CVISPageTest : CVISPlaywrightTest
{
    protected IBrowserContext Context { get; private set; } = null!;
    protected IPage Page { get; private set; } = null!;

    [SetUp]
    public async Task PlaywrightPageSetUpAsync()
    {
        Context = await Browser.NewContextAsync(BuildContextOptions()).ConfigureAwait(false);
        Page = await Context.NewPageAsync().ConfigureAwait(false);

        Logger.Info($"[Playwright] New page created for {TestContext.CurrentContext.Test.FullName}");
    }

    [TearDown]
    public async Task PlaywrightPageTearDownAsync()
    {
        if (Page is not null)
        {
            await Page.CloseAsync().ConfigureAwait(false);
        }

        if (Context is not null)
        {
            await Context.CloseAsync().ConfigureAwait(false);
        }
    }

    protected virtual BrowserNewContextOptions BuildContextOptions()
    {
        return new BrowserNewContextOptions
        {
            ViewportSize = new ViewportSize
            {
                Width = 1280,
                Height = 720
            }
        };
    }
}
