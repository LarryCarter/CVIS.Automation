using Microsoft.Data.SqlClient;
using NUnit.Framework;

namespace CVIS.FunctionalTesting.Base;

/// <summary>
/// Official base class for CVIS database automation tests.
/// Inherit from this when the test needs SQL connection helpers.
/// This class does not automatically open a connection for every test.
/// </summary>
public abstract class CvisAutomationDatabaseTestBase : CvisAutomationTestBase
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

    protected override async Task OnTestTearDownAsync()
    {
        try
        {
            foreach (var connection in _connections)
            {
                await connection.DisposeAsync().ConfigureAwait(false);
            }

            _connections.Clear();
            Logger.Info("[Database] SQL connections disposed.");
        }
        finally
        {
            await base.OnTestTearDownAsync().ConfigureAwait(false);
        }
    }
}
