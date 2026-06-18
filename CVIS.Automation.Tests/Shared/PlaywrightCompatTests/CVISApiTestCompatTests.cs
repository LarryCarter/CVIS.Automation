using CVIS.Playwright.NUnitCompat;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Shared.PlaywrightCompatTests;

[TestFixture]
[Category("CVISPlaywrightCompat")]
public sealed class CVISApiTestCompatTests : CVISApiTest
{
    [Test]
    public async Task ApiTest_ShouldCreateApiContextAndPerformRealPlaywrightRequest()
    {
        Assert.That(ApiContext, Is.Not.Null);
        await using var server = new LoopbackHttpServer();
        var response = await ApiContext.GetAsync(server.Uri.ToString());
        Assert.That(response.Ok, Is.True);
        var body = await response.TextAsync();
        Assert.That(body, Does.Contain("CVIS Playwright compatibility probe OK"));
    }

    [Test]
    public async Task ApiTest_ShouldCreateAdditionalApiRequestContext()
    {
        await using var context = await NewApiRequestContextAsync();
        Assert.That(context, Is.Not.Null);
    }
}
