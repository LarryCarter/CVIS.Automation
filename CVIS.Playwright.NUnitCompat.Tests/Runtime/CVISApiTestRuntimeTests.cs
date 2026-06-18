using CVIS.Playwright.NUnitCompat.Tests.Utilities;

namespace CVIS.Playwright.NUnitCompat.Tests.Runtime;

[TestFixture]
[Category("PlaywrightCompatUnit")]
public sealed class CVISApiTestRuntimeTests : CVISApiTest
{
    [Test]
    public void Setup_ShouldCreateDefaultApiContext()
    {
        ApiContext.Should().NotBeNull();
    }

    [Test]
    public async Task NewApiRequestContextAsync_ShouldCallLoopbackServerThroughPlaywright()
    {
        await using var server = new LoopbackHttpServer();

        var context = await NewApiRequestContextAsync(server.Uri.ToString());
        var response = await context.GetAsync("/");

        response.Ok.Should().BeTrue();

        var body = await response.TextAsync();
        body.Should().Contain("CVIS loopback ok");
    }

    [Test]
    public async Task NewApiContextAsync_ShouldCallLoopbackServerThroughPlaywright()
    {
        await using var server = new LoopbackHttpServer();

        var context = await NewApiContextAsync(server.Uri.ToString());
        var response = await context.GetAsync("/");

        response.Ok.Should().BeTrue();

        var body = await response.TextAsync();
        body.Should().Contain("CVIS loopback ok");
    }
}
