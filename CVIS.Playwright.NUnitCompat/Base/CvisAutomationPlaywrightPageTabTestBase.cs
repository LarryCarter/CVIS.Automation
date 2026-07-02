using Microsoft.Playwright;
using NUnit.Framework;

namespace CVIS.Playwright.NUnitCompat.Base;

/// <summary>
/// Official base class for CVIS Playwright tests that need a fresh browser context and page per test.
/// Inherit from this for UI/browser tests that interact with Page.
/// </summary>
public abstract class CvisAutomationPlaywrightPageTabTestBase : CvisAutomationPlaywrightBrowserTestBase
{
    protected IBrowserContext Context { get; private set; } = null!;
    protected IPage Page { get; private set; } = null!;

    protected override async Task OnTestSetUpAsync()
    {
        await base.OnTestSetUpAsync().ConfigureAwait(false);

        Context = await Browser.NewContextAsync(BuildContextOptions()).ConfigureAwait(false);
        Page = await Context.NewPageAsync().ConfigureAwait(false);

        Logger.Info($"[Playwright] New page created for {TestContext.CurrentContext.Test.FullName}");
    }

    protected override async Task OnTestTearDownAsync()
    {
        try
        {
            if (Page is not null)
            {
                await Page.CloseAsync().ConfigureAwait(false);
                Logger.Info("[Playwright] Page closed.");
            }

            if (Context is not null)
            {
                await Context.CloseAsync().ConfigureAwait(false);
                Logger.Info("[Playwright] Browser context closed.");
            }
        }
        finally
        {
            await base.OnTestTearDownAsync().ConfigureAwait(false);
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
