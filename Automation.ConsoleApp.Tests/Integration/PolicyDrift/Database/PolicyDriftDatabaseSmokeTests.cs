using Microsoft.Data.SqlClient;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Database;

public sealed class PolicyDriftDatabaseSmokeTests : UnitTestBase
{
    private readonly IConfigurationRoot _configuration;

    public PolicyDriftDatabaseSmokeTests()
    {
        _configuration = GetConfiguration();
    }

    [Fact]
    [Trait("PolicyDrift", "true")]
    [Trait("Category", "DatabaseRegression")]
    public async Task DatabaseConnection_ShouldOpenSuccessfully()
    {
        if (!IsEnabled(_configuration, "PolicyDrift:Enabled") ||
            !IsEnabled(_configuration, "PolicyDrift:RunDatabaseTests"))
        {
            return;
        }

        await using var connection = new SqlConnection(GetConnectionString());
        await connection.OpenAsync();

        connection.State.Should().Be(System.Data.ConnectionState.Open);
    }

    [Fact]
    [Trait("PolicyDrift", "true")]
    [Trait("Category", "DatabaseRegression")]
    public async Task Database_ShouldReturnCurrentServerDate()
    {
        if (!IsEnabled(_configuration, "PolicyDrift:Enabled") ||
            !IsEnabled(_configuration, "PolicyDrift:RunDatabaseTests"))
        {
            return;
        }

        await using var connection = new SqlConnection(GetConnectionString());
        await connection.OpenAsync();

        await using var command = new SqlCommand("SELECT GETDATE()", connection);
        var result = await command.ExecuteScalarAsync();

        result.Should().NotBeNull();
    }

    private string GetConnectionString()
    {
        var connectionString = _configuration["PolicyDrift:Database:ConnectionString"];
        connectionString.Should().NotBeNullOrWhiteSpace();
        return connectionString!;
    }
}
