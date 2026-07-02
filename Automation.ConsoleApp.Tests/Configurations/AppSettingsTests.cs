namespace Automation.ConsoleApp.Tests.Configurations;

public sealed class AppSettingsTests : UnitTestBase
{
    private readonly IConfigurationRoot _configuration;

    public AppSettingsTests()
    {
        _configuration = GetConfiguration();
    }

    [Theory]
    [InlineData("HealthChecks", true)]
    [InlineData("ResilientClient", true)]
    public void TestFeatureManagementSection(string key, bool expectedValue)
    {
        ValidateAppSettings("FeatureManagement", key, expectedValue);
    }

    private void ValidateAppSettings<T>(string sectionName, string key, T expectedValue)
    {
        var section = _configuration.GetSection(sectionName);
        var actualValue = section.GetValue<T>(key);

        section.Exists().Should().BeTrue($"section '{sectionName}' should exist");
        actualValue.Should().Be(expectedValue);
    }
}
