using CVIS.Playwright.NUnitCompat;
using Microsoft.Playwright;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Shared.PlaywrightCompatTests;

[TestFixture]
[Category("CVISPlaywrightCompat")]
public sealed class CVISContextDefaultsCompatTests
{
    [Test]
    public void ContextOptions_ShouldDefaultToExpectedValues()
    {
        var host = new ContextHost();
        var options = host.ContextOptions();
        Assert.That(options.Locale, Is.EqualTo("en-US"));
        Assert.That(options.ColorScheme, Is.EqualTo(ColorScheme.Light));
    }
    private sealed class ContextHost : CVISContextTest { }
}
