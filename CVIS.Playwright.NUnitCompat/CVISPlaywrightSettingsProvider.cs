using Microsoft.Playwright;

namespace CVIS.Playwright.NUnitCompat;

public static class CVISPlaywrightSettingsProvider
{
    public static string BrowserName
    {
        get
        {
            var browserFromEnv = Environment.GetEnvironmentVariable("BROWSER")?.ToLowerInvariant();
            if (!string.IsNullOrWhiteSpace(browserFromEnv) && !browserFromEnv.StartsWith("/vscode/"))
            {
                ValidateBrowserName(browserFromEnv, "'BROWSER' environment variable");
                return browserFromEnv;
            }
            var cvisBrowser = Environment.GetEnvironmentVariable("CVIS_PLAYWRIGHT_BROWSER")?.ToLowerInvariant();
            if (!string.IsNullOrWhiteSpace(cvisBrowser))
            {
                ValidateBrowserName(cvisBrowser, "'CVIS_PLAYWRIGHT_BROWSER' environment variable");
                return cvisBrowser;
            }
            return BrowserType.Chromium;
        }
    }

    public static string TestIdAttribute => Environment.GetEnvironmentVariable("CVIS_PLAYWRIGHT_TEST_ID_ATTRIBUTE") ?? "data-testid";

    public static float? ExpectTimeout
    {
        get
        {
            var raw = Environment.GetEnvironmentVariable("CVIS_PLAYWRIGHT_EXPECT_TIMEOUT");
            return float.TryParse(raw, out var timeout) ? timeout : null;
        }
    }

    public static BrowserTypeLaunchOptions LaunchOptions
    {
        get
        {
            var options = new BrowserTypeLaunchOptions();
            if (Environment.GetEnvironmentVariable("HEADED") == "1") options.Headless = false;
            var cvisHeadless = Environment.GetEnvironmentVariable("CVIS_PLAYWRIGHT_HEADLESS");
            if (bool.TryParse(cvisHeadless, out var headless)) options.Headless = headless;
            var channel = Environment.GetEnvironmentVariable("CVIS_PLAYWRIGHT_CHANNEL");
            if (!string.IsNullOrWhiteSpace(channel)) options.Channel = channel;
            return options;
        }
    }

    public static void ValidateBrowserName(string browserName, string source)
    {
        if (browserName is BrowserType.Chromium or BrowserType.Firefox or BrowserType.Webkit) return;
        throw new ArgumentException($"Invalid browser name from {source}. Supported browsers: '{BrowserType.Chromium}', '{BrowserType.Firefox}', and '{BrowserType.Webkit}'. Actual browser: '{browserName}'.");
    }
}
