using CVIS.Playwright.NUnitCompat;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Shared.PlaywrightCompatTests;

[TestFixture]
[Category("CVISPlaywrightCompat")]
public sealed class CVISPageTestBrowserCompatTests : CVISPageTest
{
    [Test]
    [Explicit("Requires Playwright browsers installed. Run manually when validating browser-backed CVISPageTest.")]
    public async Task PageTest_ShouldCreateBrowserContextAndPage()
    {
        Assert.That(Browser, Is.Not.Null);
        Assert.That(Context, Is.Not.Null);
        Assert.That(Page, Is.Not.Null);
        await Page.SetContentAsync("<html><head><title>CVIS</title></head><body><h1 data-testid='title'>OK</h1></body></html>");
        await Expect(Page).ToHaveTitleAsync("CVIS");
    }
}
