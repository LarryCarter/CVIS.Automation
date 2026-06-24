using Microsoft.Playwright;
using CVIS.Playwright.NUnitCompat;

namespace CVIS.Playwright.NUnitCompat.Tests.Browser;

[TestFixture]
[Category("PlaywrightCompatUnit")]
public sealed class CVISContextOptionsTests
{
    [Test]
    public void ContextOptions_ShouldDefaultToEnglishLightColorScheme()
    {
        var test = new CVISContextTest();

        var options = test.ContextOptions();

        options.Locale.Should().Be("en-US");
        options.ColorScheme.Should().Be(ColorScheme.Light);
    }
}
