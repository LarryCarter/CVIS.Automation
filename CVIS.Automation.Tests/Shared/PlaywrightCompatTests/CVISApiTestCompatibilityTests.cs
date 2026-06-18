using CVIS.Playwright.NUnitCompat;
using FluentAssertions;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Shared.PlaywrightCompatTests;

[TestFixture]
[Category("PlaywrightCompatibility")]
public sealed class CVISApiTestCompatibilityTests : CVISApiTest
{
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
