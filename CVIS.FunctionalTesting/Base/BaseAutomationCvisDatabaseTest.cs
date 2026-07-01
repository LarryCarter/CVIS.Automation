using Microsoft.Data.SqlClient;
using NUnit.Framework;

namespace CVIS.FunctionalTesting.Base;

/// <summary>
/// Base class for CVIS database automation tests.
/// Provides connection-string access and helper methods.
/// This class does not automatically open a SQL connection for every test.
/// Tests opt in by calling OpenDatabaseConnectionAsync or AssertDatabaseConnectionCanOpenAsync.
/// </summary>
[TestFixture]
public abstract class BaseAutomationCvisDatabaseTest : BaseAutomationCvisTest
{
    private readonly List<SqlConnection> _connections = new();

    protected string DatabaseConnectionString => Config.DatabaseConnection;

    protected async Task<SqlConnection> OpenDatabaseConnectionAsync(CancellationToken cancellationToken = default)
    {
        if (string.IsNullOrWhiteSpace(DatabaseConnectionString))
        {
            throw new InvalidOperationException(
                "DatabaseConnection is empty. Configure it in appsettings.test.json before running database tests.");
        }

        var connection = new SqlConnection(DatabaseConnectionString);
        await connection.OpenAsync(cancellationToken).ConfigureAwait(false);

        _connections.Add(connection);
        Logger.Info("[Database] SQL connection opened.");

        return connection;
    }

    protected async Task AssertDatabaseConnectionCanOpenAsync(CancellationToken cancellationToken = default)
    {
        await using var connection = new SqlConnection(DatabaseConnectionString);
        await connection.OpenAsync(cancellationToken).ConfigureAwait(false);

        Assert.That(connection.State, Is.EqualTo(System.Data.ConnectionState.Open));
    }

    [TearDown]
    public virtual async Task DatabaseTestTearDownAsync()
    {
        foreach (var connection in _connections)
        {
            await connection.DisposeAsync().ConfigureAwait(false);
        }

        _connections.Clear();
        Logger.Info("[Database] SQL connections disposed.");
    }
}
