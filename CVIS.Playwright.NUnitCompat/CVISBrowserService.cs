using System.Collections.Concurrent;
using Microsoft.Playwright;
using CVIS.Playwright.NUnitCompat;

namespace CVIS.Playwright.NUnitCompat;

public sealed class CVISBrowserService
{
    private static readonly ConcurrentDictionary<string, Lazy<Task<CVISBrowserService>>> Services = new();

    private CVISBrowserService(IBrowser browser)
    {
        Browser = browser;
    }

    public IBrowser Browser { get; }

    public static Task<CVISBrowserService> RegisterAsync(
        IBrowserType browserType,
        (string Endpoint, BrowserTypeConnectOptions? Options)? connectOptions,
        BrowserTypeLaunchOptions? launchOptions)
    {
        var key = CreateKey(browserType.Name, connectOptions, launchOptions);

        return Services.GetOrAdd(
            key,
            _ => new Lazy<Task<CVISBrowserService>>(
                () => CreateAsync(browserType, connectOptions, launchOptions))).Value;
    }

    public static async Task CloseAllAsync()
    {
        foreach (var service in Services.Values)
        {
            var resolved = await service.Value.ConfigureAwait(false);
            await resolved.Browser.CloseAsync().ConfigureAwait(false);
        }

        Services.Clear();
    }

    private static async Task<CVISBrowserService> CreateAsync(
        IBrowserType browserType,
        (string Endpoint, BrowserTypeConnectOptions? Options)? connectOptions,
        BrowserTypeLaunchOptions? launchOptions)
    {
        IBrowser browser;

        if (connectOptions.HasValue)
        {
            browser = await browserType.ConnectAsync(
                connectOptions.Value.Endpoint,
                connectOptions.Value.Options).ConfigureAwait(false);
        }
        else
        {
            browser = await browserType.LaunchAsync(launchOptions).ConfigureAwait(false);
        }

        return new CVISBrowserService(browser);
    }

    private static string CreateKey(
        string browserName,
        (string Endpoint, BrowserTypeConnectOptions? Options)? connectOptions,
        BrowserTypeLaunchOptions? launchOptions)
    {
        var connectKey = connectOptions.HasValue
            ? connectOptions.Value.Endpoint
            : "launch";

        var headedKey = launchOptions?.Headless?.ToString() ?? "default";
        var slowMoKey = launchOptions?.SlowMo?.ToString() ?? "none";

        return $"{browserName}|{connectKey}|headless:{headedKey}|slowmo:{slowMoKey}";
    }
}
