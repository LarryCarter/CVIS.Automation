using CVIS.Playwright.NUnitCompat;
using Microsoft.Playwright;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Shared.PlaywrightCompatTests;

[TestFixture]
[Category("CVISPlaywrightCompat")]
public sealed class CVISPlaywrightSettingsProviderTests
{
    [Test]
    public void BrowserName_ShouldDefaultToChromium()
    {
        using var scope = new EnvironmentScope("BROWSER", null);
        using var cvisScope = new EnvironmentScope("CVIS_PLAYWRIGHT_BROWSER", null);
        Assert.That(CVISPlaywrightSettingsProvider.BrowserName, Is.EqualTo(BrowserType.Chromium));
    }

    [Test]
    public void BrowserName_ShouldReadCvisBrowserEnvironmentVariable()
    {
        using var scope = new EnvironmentScope("BROWSER", null);
        using var cvisScope = new EnvironmentScope("CVIS_PLAYWRIGHT_BROWSER", BrowserType.Firefox);
        Assert.That(CVISPlaywrightSettingsProvider.BrowserName, Is.EqualTo(BrowserType.Firefox));
    }

    [Test]
    public void BrowserName_ShouldRejectInvalidBrowser()
    {
        using var scope = new EnvironmentScope("BROWSER", "not-a-browser");
        Assert.Throws<ArgumentException>(() => _ = CVISPlaywrightSettingsProvider.BrowserName);
    }

    [Test]
    public void LaunchOptions_ShouldHonorHeadedEnvironmentVariable()
    {
        using var scope = new EnvironmentScope("HEADED", "1");
        Assert.That(CVISPlaywrightSettingsProvider.LaunchOptions.Headless, Is.False);
    }

    private sealed class EnvironmentScope : IDisposable
    {
        private readonly string _name;
        private readonly string? _originalValue;
        public EnvironmentScope(string name, string? value) { _name = name; _originalValue = Environment.GetEnvironmentVariable(name); Environment.SetEnvironmentVariable(name, value); }
        public void Dispose() => Environment.SetEnvironmentVariable(_name, _originalValue);
    }
}
