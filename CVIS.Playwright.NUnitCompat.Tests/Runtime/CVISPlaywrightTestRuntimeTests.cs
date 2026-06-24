using CVIS.Playwright.NUnitCompat;
namespace CVIS.Playwright.NUnitCompat.Tests.Runtime;

[TestFixture]
[Category("PlaywrightCompatUnit")]
public sealed class CVISPlaywrightTestRuntimeTests : CVISPlaywrightTest
{
    [Test]
    public void Setup_ShouldInitializePlaywrightBrowserNameAndBrowserType()
    {
        Playwright.Should().NotBeNull();
        BrowserName.Should().BeOneOf("chromium", "firefox", "webkit");
        BrowserType.Should().NotBeNull();
        Settings.Should().NotBeNull();
    }
}
