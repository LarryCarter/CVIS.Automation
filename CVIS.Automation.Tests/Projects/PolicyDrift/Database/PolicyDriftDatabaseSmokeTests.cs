using CVIS.Automation.Tests.Shared.Database;
using CVIS.Automation.Tests.Shared.Helpers;
using FluentAssertions;
using Microsoft.Data.SqlClient;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Projects.PolicyDrift.Database;

[TestFixture]
[Category("PolicyDrift")]
[Category("DatabaseRegression")]
public sealed class PolicyDriftDatabaseSmokeTests
{
    private const string ProjectName = "PolicyDrift";
    private TestConfig _config = null!;

    [SetUp]
    public void Setup()
    {
        _config = TestConfig.Load();
    }

    [Test]
    public async Task DatabaseConnection_ShouldOpenSuccessfully()
    {
        var project = _config.GetProject(ProjectName);

        if (!project.Enabled || !_config.TestSettings.RunDatabaseTests)
        {
            Assert.Ignore("PolicyDrift database tests are disabled in appsettings.test.json.");
        }

        var factory = new SqlConnectionFactory(project.Database.ConnectionString);

        await using var connection = factory.CreateConnection();
        await connection.OpenAsync();

        connection.State.Should().Be(System.Data.ConnectionState.Open);
    }

    [Test]
    public async Task Database_ShouldReturnCurrentServerDate()
    {
        var project = _config.GetProject(ProjectName);

        if (!project.Enabled || !_config.TestSettings.RunDatabaseTests)
        {
            Assert.Ignore("PolicyDrift database tests are disabled in appsettings.test.json.");
        }

        var factory = new SqlConnectionFactory(project.Database.ConnectionString);

        await using var connection = factory.CreateConnection();
        await connection.OpenAsync();

        await using var command = new SqlCommand("SELECT GETDATE()", connection);
        var result = await command.ExecuteScalarAsync();

        result.Should().NotBeNull();
    }
}
