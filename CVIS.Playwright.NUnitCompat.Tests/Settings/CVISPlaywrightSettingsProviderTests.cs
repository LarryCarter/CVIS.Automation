using CVIS.Playwright.NUnitCompat.Tests.Utilities;
using CVIS.Playwright.NUnitCompat;

namespace CVIS.Playwright.NUnitCompat.Tests.Settings;

[TestFixture]
[Category("PlaywrightCompatUnit")]
public sealed class CVISPlaywrightSettingsProviderTests
{
    [Test]
    public void FromEnvironment_WhenUnset_ShouldDefaultToChromiumHeadless()
    {
        using var env = new EnvironmentVariableScope()
            .Set("BROWSER", null)
            .Set("HEADED", null)
            .Set("PWDEBUG", null)
            .Set("EXPECT_TIMEOUT", null)
            .Set("SLOW_MO", null)
            .Set("TEST_ID_ATTRIBUTE", null);

        var settings = CVISPlaywrightSettingsProvider.FromEnvironment();

        settings.BrowserName.Should().Be("chromium");
        settings.Headed.Should().BeFalse();
        settings.Headless.Should().BeTrue();
        settings.ExpectTimeout.Should().BeNull();
        settings.SlowMo.Should().BeNull();
        settings.TestIdAttribute.Should().Be("data-testid");
    }

    [TestCase("chromium")]
    [TestCase("firefox")]
    [TestCase("webkit")]
    public void FromEnvironment_WhenBrowserSet_ShouldAcceptSupportedBrowser(string browser)
    {
        using var env = new EnvironmentVariableScope()
            .Set("BROWSER", browser);

        var settings = CVISPlaywrightSettingsProvider.FromEnvironment();

        settings.BrowserName.Should().Be(browser);
    }

    [Test]
    public void FromEnvironment_WhenInvalidBrowserSet_ShouldThrow()
    {
        using var env = new EnvironmentVariableScope()
            .Set("BROWSER", "bad-browser");

        Action action = () => CVISPlaywrightSettingsProvider.FromEnvironment();

        action.Should().Throw<InvalidOperationException>()
            .WithMessage("*bad-browser*");
    }

    [TestCase("1")]
    [TestCase("true")]
    [TestCase("yes")]
    public void FromEnvironment_WhenHeadedSet_ShouldSetHeadedAndDisableHeadless(string value)
    {
        using var env = new EnvironmentVariableScope()
            .Set("HEADED", value);

        var settings = CVISPlaywrightSettingsProvider.FromEnvironment();

        settings.Headed.Should().BeTrue();
        settings.Headless.Should().BeFalse();
    }

    [Test]
    public void FromEnvironment_WhenPwDebugSet_ShouldSetHeadedAndDisableHeadless()
    {
        using var env = new EnvironmentVariableScope()
            .Set("PWDEBUG", "1");

        var settings = CVISPlaywrightSettingsProvider.FromEnvironment();

        settings.Headed.Should().BeTrue();
        settings.Headless.Should().BeFalse();
    }

    [Test]
    public void FromEnvironment_WhenTimeoutSlowMoAndTestIdSet_ShouldMapValues()
    {
        using var env = new EnvironmentVariableScope()
            .Set("EXPECT_TIMEOUT", "2500")
            .Set("SLOW_MO", "100")
            .Set("TEST_ID_ATTRIBUTE", "data-cvis-id");

        var settings = CVISPlaywrightSettingsProvider.FromEnvironment();

        settings.ExpectTimeout.Should().Be(2500);
        settings.SlowMo.Should().Be(100);
        settings.TestIdAttribute.Should().Be("data-cvis-id");
    }

    [Test]
    public void ToLaunchOptions_ShouldMapHeadlessAndSlowMo()
    {
        var settings = new CVISPlaywrightSettings
        {
            Headless = false,
            SlowMo = 75
        };

        var options = CVISPlaywrightSettingsProvider.ToLaunchOptions(settings);

        options.Headless.Should().BeFalse();
        options.SlowMo.Should().Be(75);
    }
}
