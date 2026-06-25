using CVIS.FunctionalTesting.Base;
using Microsoft.Playwright;
using NUnit.Framework;

namespace CVIS.Playwright.NUnitCompat.Base;

/// <summary>
/// Browser lane base class. Use only when the test needs Playwright.
/// Plain functional tests should inherit BaseFunctionalTest instead.
/// </summary>
[TestFixture]
public abstract class CVISPlaywrightTest : BaseFunctionalTest
{
    protected IPlaywright PlaywrightInstance { get; private set; } = null!;
    protected IBrowser Browser { get; private set; } = null!;

    [OneTimeSetUp]
    public async Task PlaywrightFixtureSetUpAsync()
    {
        PlaywrightInstance = await Microsoft.Playwright.Playwright.CreateAsync().ConfigureAwait(false);
        Browser = await LaunchBrowserAsync(PlaywrightInstance).ConfigureAwait(false);

        Logger.Info($"[Playwright] Browser launched: {Browser.BrowserType.Name}");
    }

    [OneTimeTearDown]
    public async Task PlaywrightFixtureTearDownAsync()
    {
        try
        {
            if (Browser is not null)
            {
                await Browser.CloseAsync().ConfigureAwait(false);
                Logger.Info("[Playwright] Browser closed");
            }
        }
        finally
        {
            PlaywrightInstance?.Dispose();
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
