using CVIS.Playwright.Automation.Shared.Api;
using FluentAssertions;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Projects.PolicyDrift.Api;

[TestFixture]
[Category("PolicyDrift")]
[Category("CyberArk")]
[Category("ApiRegression")]
public sealed class CyberArkEpvApiTests : PlaywrightApiFixture
{
    private const string ProjectName = "PolicyDrift";

    [Test]
    public async Task GetPlatforms_ShouldReturnSuccessfulResponse_WhenCyberArkIsAvailable()
    {
        var project = Config.GetProject(ProjectName);

        if (!project.Enabled || !Config.TestSettings.RunApiTests)
        {
            Assert.Ignore("PolicyDrift CyberArk API tests are disabled in appsettings.test.json.");
        }

        await using var request = await CreateApiRequestContextAsync(
            project.CyberArk.BaseUrl,
            project.CyberArk.ResolveToken());

        var response = await request.GetAsync("/PasswordVault/API/Platforms");

        response.Status.Should().BeInRange(200, 299);

        var body = await response.TextAsync();

        body.Should().NotBeNullOrWhiteSpace();
    }
}
