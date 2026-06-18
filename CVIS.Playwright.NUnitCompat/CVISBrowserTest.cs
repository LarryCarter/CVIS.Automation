using Microsoft.Playwright;
using NUnit.Framework;
using NUnit.Framework.Interfaces;

namespace CVIS.Playwright.NUnitCompat;

public abstract class CVISBrowserTest : CVISPlaywrightTest
{
    private readonly List<IBrowserContext> _contexts = new();
    public IBrowser Browser { get; private set; } = null!;

    [SetUp]
    public async Task CVISBrowserSetupAsync()
    {
        var connectOptions = await ConnectOptionsAsync().ConfigureAwait(false);
        if (connectOptions is not null)
        {
            Browser = await BrowserType.ConnectAsync(connectOptions.Value.wsEndpoint, connectOptions.Value.options).ConfigureAwait(false);
            return;
        }
        Browser = await CVISBrowserService.GetOrLaunchAsync(BrowserType, await LaunchOptionsAsync().ConfigureAwait(false)).ConfigureAwait(false);
    }

    [TearDown]
    public async Task CVISBrowserTearDownAsync()
    {
        if (TestContext.CurrentContext.Result.Outcome.Status == TestStatus.Passed)
        {
            foreach (var context in _contexts) await context.CloseAsync().ConfigureAwait(false);
        }
        _contexts.Clear();
    }

    public async Task<IBrowserContext> NewContext(BrowserNewContextOptions? options = null)
    {
        var context = await Browser.NewContextAsync(options).ConfigureAwait(false);
        _contexts.Add(context);
        return context;
    }

    public virtual Task<BrowserTypeLaunchOptions> LaunchOptionsAsync() => Task.FromResult(CVISPlaywrightSettingsProvider.LaunchOptions);
    public virtual Task<(string wsEndpoint, BrowserTypeConnectOptions? options)?> ConnectOptionsAsync() => Task.FromResult<(string wsEndpoint, BrowserTypeConnectOptions? options)?>(null);
}
