using CVIS.Playwright.NUnitCompat;
namespace CVIS.Playwright.NUnitCompat.Tests.Browser;

[TestFixture]
[Category("PlaywrightCompatUnit")]
public sealed class CVISBrowserLaunchOptionsTests
{
    private sealed class TestBrowserTest : CVISBrowserTest
    {
    }

    [Test]
    public async Task DefaultConnectOptionsAsync_ShouldReturnNull()
    {
        var test = new TestBrowserTest();

        var options = await test.ConnectOptionsAsync();

        options.Should().BeNull();
    }

    [Test]
    public async Task DefaultLaunchOptionsAsync_ShouldReturnNull()
    {
        var test = new TestBrowserTest();

        var options = await test.LaunchOptionsAsync();

        options.Should().BeNull();
    }
}
