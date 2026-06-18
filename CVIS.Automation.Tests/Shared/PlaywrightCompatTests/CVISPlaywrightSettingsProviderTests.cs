using CVIS.Playwright.NUnitCompat;
using FluentAssertions;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Shared.PlaywrightCompatTests;

[TestFixture]
[Category("PlaywrightCompatibility")]
public sealed class CVISPlaywrightSettingsProviderTests
{
    [Test]
    public void FromEnvironment_ShouldDefaultToChromiumHeadless()
    {
        Environment.SetEnvironmentVariable("BROWSER", null);
        Environment.SetEnvironmentVariable("HEADED", null);
        Environment.SetEnvironmentVariable("PWDEBUG", null);

        var settings = CVISPlaywrightSettingsProvider.FromEnvironment();

        settings.BrowserName.Should().Be("chromium");
        settings.Headless.Should().BeTrue();
        settings.TestIdAttribute.Should().Be("data-testid");
    }

    [Test]
    public void FromEnvironment_ShouldRespectBrowserAndHeaded()
    {
        Environment.SetEnvironmentVariable("BROWSER", "firefox");
        Environment.SetEnvironmentVariable("HEADED", "1");

        var settings = CVISPlaywrightSettingsProvider.FromEnvironment();

        settings.BrowserName.Should().Be("firefox");
        settings.Headed.Should().BeTrue();
        settings.Headless.Should().BeFalse();

        Environment.SetEnvironmentVariable("BROWSER", null);
        Environment.SetEnvironmentVariable("HEADED", null);
    }

    [Test]
    public void FromEnvironment_ShouldRejectInvalidBrowser()
    {
        Environment.SetEnvironmentVariable("BROWSER", "invalid-browser");

        Action action = () => CVISPlaywrightSettingsProvider.FromEnvironment();

        action.Should().Throw<InvalidOperationException>();

        Environment.SetEnvironmentVariable("BROWSER", null);
    }
}
