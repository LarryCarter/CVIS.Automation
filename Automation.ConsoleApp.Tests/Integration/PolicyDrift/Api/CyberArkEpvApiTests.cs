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
    [Trait("CyberArk", "true")]
    [Trait("ApiRegression", "true")]
    public void GetPlatforms_ShouldHavePolicyDriftConfigurationAvailable()
    {
        _configuration.Should().NotBeNull();
    }
}
