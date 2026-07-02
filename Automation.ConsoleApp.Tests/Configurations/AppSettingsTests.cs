namespace Automation.ConsoleApp.Tests.Configurations;

/// <summary>
/// Validates required appsettings.json configuration for generated xUnit tests.
/// </summary>
public sealed class AppSettingsTests : UnitTestBase
{
    private readonly IConfigurationRoot _configuration = GetConfiguration();

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
        actualValue.Should().NotBeNull();
        actualValue.Should().Be(expectedValue);
    }
}
