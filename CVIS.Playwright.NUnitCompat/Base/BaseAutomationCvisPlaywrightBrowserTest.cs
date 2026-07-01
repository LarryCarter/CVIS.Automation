using CVIS.FunctionalTesting.Base;
using Microsoft.Playwright;

namespace CVIS.Playwright.NUnitCompat.Base;

/// <summary>
/// Official base class for CVIS browser-level Playwright tests.
/// Inherit from this when a test needs Playwright and a shared browser, but not a fresh page per test.
/// For a fresh page per test, use BaseAutomationCvisPlaywrightPageTabTest.
/// </summary>
public abstract class BaseAutomationCvisPlaywrightBrowserTest : BaseAutomationCvisTest
{
    protected IPlaywright PlaywrightInstance { get; private set; } = null!;
    protected IBrowser Browser { get; private set; } = null!;

    protected override async Task OnFixtureSetUpAsync()
    {
        await base.OnFixtureSetUpAsync().ConfigureAwait(false);

        PlaywrightInstance = await Microsoft.Playwright.Playwright.CreateAsync().ConfigureAwait(false);
        Browser = await LaunchBrowserAsync(PlaywrightInstance).ConfigureAwait(false);

        Logger.Info($"[Playwright] Browser launched: {Browser.BrowserType.Name}");
    }

    protected override async Task OnFixtureTearDownAsync()
    {
        try
        {
            if (Browser is not null)
            {
                await Browser.CloseAsync().ConfigureAwait(false);
                Logger.Info("[Playwright] Browser closed.");
            }
        }
        finally
        {
            PlaywrightInstance?.Dispose();
            await base.OnFixtureTearDownAsync().ConfigureAwait(false);
        }
    }

    protected virtual Task<IBrowser> LaunchBrowserAsync(IPlaywright playwright)
    {
        return playwright.Chromium.LaunchAsync(new BrowserTypeLaunchOptions
        {
            Headless = true,
            SlowMo = 0
        });
    }
}
