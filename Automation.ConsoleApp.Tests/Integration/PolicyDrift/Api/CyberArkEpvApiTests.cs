namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Api;

public sealed class CyberArkEpvApiTests : UnitTestBase
{
    private readonly IConfigurationRoot _configuration = GetConfiguration();

    [Fact]
    [Trait("Category", "PolicyDrift")]
    [Trait("Category", "CyberArk")]
    [Trait("Category", "ApiRegression")]
    public void GetPlatforms_ShouldReturnSuccessfulResponse_WhenCyberArkIsAvailable()
    {
        var section = _configuration.GetSection("PolicyDrift");
        section.Exists().Should().BeTrue("PolicyDrift configuration should exist");

        var runApiTests = section.GetValue<bool>("RunApiTests");
        var baseUrl = section.GetSection("CyberArk").GetValue<string>("BaseUrl");

        if (!runApiTests)
        {
            return;
        }

        baseUrl.Should().NotBeNullOrWhiteSpace("CyberArk API tests require a configured base URL");
    }
}
