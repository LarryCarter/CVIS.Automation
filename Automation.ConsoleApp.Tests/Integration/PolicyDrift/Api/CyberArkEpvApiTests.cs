using FluentAssertions;
using Microsoft.Extensions.Configuration;

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
    public void GetPlatforms_PolicyDrift_ShouldHavePolicyDriftConfigurationAvailable()
    {
        _configuration.Should().NotBeNull();
    }

    [Fact]
[Trait("CyberArk", "true")]
    public void GetPlatforms_CyberArk_ShouldHavePolicyDriftConfigurationAvailable()
    {
        _configuration.Should().NotBeNull();
    }

    [Fact]
[Trait("ApiRegression", "true")]
    public void GetPlatforms_ApiRegression_ShouldHavePolicyDriftConfigurationAvailable()
    {
        _configuration.Should().NotBeNull();
    }
}
