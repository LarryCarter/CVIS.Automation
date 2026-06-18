using Microsoft.Playwright;
using NUnit.Framework;

namespace CVIS.Playwright.NUnitCompat;

/// <summary>
/// CVIS equivalent of Microsoft.Playwright.NUnit.BrowserTest.
/// Provides Browser, NewContext, LaunchOptionsAsync, and ConnectOptionsAsync.
/// </summary>
public class CVISBrowserTest : CVISPlaywrightTest
{
    private readonly List<IBrowserContext> _contexts = new();

    public IBrowser Browser { get; private set; } = null!;

    public async Task<IBrowserContext> NewContext(BrowserNewContextOptions? options = null)
    {
        var context = await Browser.NewContextAsync(options).ConfigureAwait(false);
        _contexts.Add(context);
        return context;
    }

    [SetUp]
    public async Task CVISBrowserSetupAsync()
    {
        var launchOptions = await LaunchOptionsAsync().ConfigureAwait(false)
            ?? CVISPlaywrightSettingsProvider.ToLaunchOptions(Settings);

        var service = await CVISBrowserService.RegisterAsync(
            BrowserType,
            await ConnectOptionsAsync().ConfigureAwait(false),
            launchOptions).ConfigureAwait(false);

        Browser = service.Browser;
    }

    [TearDown]
    public async Task CVISBrowserTearDownAsync()
    {
        if (TestOk())
        {
            foreach (var context in _contexts)
            {
                await context.CloseAsync().ConfigureAwait(false);
            }
        }

        _contexts.Clear();
        Browser = null!;
    }

    public virtual Task<(string Endpoint, BrowserTypeConnectOptions? Options)?> ConnectOptionsAsync() =>
        Task.FromResult<(string Endpoint, BrowserTypeConnectOptions? Options)?>(null);

    public virtual Task<BrowserTypeLaunchOptions?> LaunchOptionsAsync() =>
        Task.FromResult<BrowserTypeLaunchOptions?>(null);
}
