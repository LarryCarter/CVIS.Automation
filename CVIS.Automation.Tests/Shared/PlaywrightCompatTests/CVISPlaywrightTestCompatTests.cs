using CVIS.Playwright.NUnitCompat;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Shared.PlaywrightCompatTests;

[TestFixture]
[Category("CVISPlaywrightCompat")]
public sealed class CVISPlaywrightTestCompatTests : CVISPlaywrightTest
{
    [Test]
    public void PlaywrightTest_ShouldInitializeRuntimeAndBrowserType()
    {
        Assert.That(Playwright, Is.Not.Null);
        Assert.That(BrowserName, Is.Not.Empty);
        Assert.That(BrowserType, Is.Not.Null);
    }
}
