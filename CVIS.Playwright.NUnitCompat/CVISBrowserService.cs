using System.Collections.Concurrent;
using Microsoft.Playwright;

namespace CVIS.Playwright.NUnitCompat;

public sealed class CVISBrowserService
{
    private static readonly ConcurrentDictionary<string, Lazy<Task<IBrowser>>> Browsers = new();

    public static Task<IBrowser> GetOrLaunchAsync(IBrowserType browserType, BrowserTypeLaunchOptions launchOptions)
    {
        var key = CreateKey(browserType.Name, launchOptions);
        var lazy = Browsers.GetOrAdd(key, _ => new Lazy<Task<IBrowser>>(() => browserType.LaunchAsync(launchOptions), LazyThreadSafetyMode.ExecutionAndPublication));
        return lazy.Value;
    }

    public static async Task CloseAllAsync()
    {
        foreach (var pair in Browsers)
        {
            if (!pair.Value.IsValueCreated) continue;
            try { var browser = await pair.Value.Value.ConfigureAwait(false); await browser.CloseAsync().ConfigureAwait(false); } catch { }
        }
        Browsers.Clear();
    }

    private static string CreateKey(string browserName, BrowserTypeLaunchOptions options)
    {
        var headless = options.Headless?.ToString() ?? "default";
        var channel = options.Channel ?? "default";
        return $"{browserName}|headless={headless}|channel={channel}";
    }
}
