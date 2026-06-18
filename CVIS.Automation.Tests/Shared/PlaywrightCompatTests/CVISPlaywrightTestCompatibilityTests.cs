using CVIS.Playwright.NUnitCompat;
using FluentAssertions;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Shared.PlaywrightCompatTests;

[TestFixture]
[Category("PlaywrightCompatibility")]
public sealed class CVISPlaywrightTestCompatibilityTests : CVISPlaywrightTest
{
    [Test]
    public void PlaywrightSetup_ShouldInitializeRuntimeAndBrowserType()
    {
        Playwright.Should().NotBeNull();
        BrowserType.Should().NotBeNull();
        BrowserName.Should().BeOneOf("chromium", "firefox", "webkit");
    }
}
