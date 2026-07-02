using Microsoft.Playwright;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Api;

public sealed class CyberArkEpvApiTests : UnitTestBase
{
    private readonly IConfigurationRoot _configuration;

    public CyberArkEpvApiTests()
    {
        _configuration = GetConfiguration();
    }

    [Fact]
    [Trait("PolicyDrift", "true")]
    [Trait("Category", "CyberArk")]
    [Trait("Category", "ApiRegression")]
    public async Task GetPlatforms_ShouldReturnSuccessfulResponse_WhenCyberArkIsAvailable()
    {
        if (!IsEnabled(_configuration, "PolicyDrift:Enabled") ||
            !IsEnabled(_configuration, "PolicyDrift:RunApiTests"))
        {
            return;
        }

        var baseUrl = _configuration["PolicyDrift:CyberArk:BaseUrl"];
        var token = _configuration["PolicyDrift:CyberArk:Token"];

        baseUrl.Should().NotBeNullOrWhiteSpace();

        using var playwright = await Playwright.CreateAsync();
        await using var request = await playwright.APIRequest.NewContextAsync(new APIRequestNewContextOptions
        {
            BaseURL = baseUrl,
            ExtraHTTPHeaders = string.IsNullOrWhiteSpace(token)
                ? new Dictionary<string, string>()
                : new Dictionary<string, string> { ["Authorization"] = token }
        });

        var response = await request.GetAsync("/PasswordVault/API/Platforms");
        response.Status.Should().BeInRange(200, 299);

        var body = await response.TextAsync();
        body.Should().NotBeNullOrWhiteSpace();
    }
}
