using Microsoft.Playwright;
using CVIS.Playwright.NUnitCompat;

namespace CVIS.Playwright.NUnitCompat;

public sealed record CVISPlaywrightSettings
{
    public string BrowserName { get; init; } = "chromium";
    public bool Headed { get; init; }
    public bool Headless { get; init; } = true;
    public float? ExpectTimeout { get; init; }
    public float? SlowMo { get; init; }
    public string TestIdAttribute { get; init; } = "data-testid";
}

public static class CVISPlaywrightSettingsProvider
{
    private static readonly HashSet<string> ValidBrowsers =
        new(StringComparer.OrdinalIgnoreCase)
        {
            "chromium",
            "firefox",
            "webkit"
        };

    public static CVISPlaywrightSettings Current => FromEnvironment();

    public static CVISPlaywrightSettings FromEnvironment()
    {
        var browserName = Environment.GetEnvironmentVariable("BROWSER");

        if (string.IsNullOrWhiteSpace(browserName))
        {
            browserName = "chromium";
        }

        browserName = browserName.Trim().ToLowerInvariant();

        if (!ValidBrowsers.Contains(browserName))
        {
            throw new InvalidOperationException(
                $"Invalid BROWSER value '{browserName}'. Expected chromium, firefox, or webkit.");
        }

        var headed = ReadBoolean("HEADED") || ReadBoolean("PWDEBUG");
        var expectTimeout = ReadNullableFloat("EXPECT_TIMEOUT");
        var slowMo = ReadNullableFloat("SLOW_MO");

        var testIdAttribute = Environment.GetEnvironmentVariable("TEST_ID_ATTRIBUTE");

        if (string.IsNullOrWhiteSpace(testIdAttribute))
        {
            testIdAttribute = "data-testid";
        }

        return new CVISPlaywrightSettings
        {
            BrowserName = browserName,
            Headed = headed,
            Headless = !headed,
            ExpectTimeout = expectTimeout,
            SlowMo = slowMo,
            TestIdAttribute = testIdAttribute
        };
    }

    public static BrowserTypeLaunchOptions ToLaunchOptions(CVISPlaywrightSettings settings)
    {
        return new BrowserTypeLaunchOptions
        {
            Headless = settings.Headless,
            SlowMo = settings.SlowMo
        };
    }

    private static bool ReadBoolean(string name)
    {
        var value = Environment.GetEnvironmentVariable(name);

        if (string.IsNullOrWhiteSpace(value))
        {
            return false;
        }

        return value.Equals("1", StringComparison.OrdinalIgnoreCase)
            || value.Equals("true", StringComparison.OrdinalIgnoreCase)
            || value.Equals("yes", StringComparison.OrdinalIgnoreCase);
    }

    private static float? ReadNullableFloat(string name)
    {
        var value = Environment.GetEnvironmentVariable(name);

        if (string.IsNullOrWhiteSpace(value))
        {
            return null;
        }

        if (float.TryParse(value, out var parsed))
        {
            return parsed;
        }

        return null;
    }
}
