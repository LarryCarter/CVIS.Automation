using Microsoft.Data.SqlClient;

namespace CVIS.Playwright.Automation.Shared.Database;

public static class DbAssert
{
    public static async Task<int> ExecuteScalarIntAsync(
        SqlConnection connection,
        string sql,
        params SqlParameter[] parameters)
    {
        await using var command = new SqlCommand(sql, connection);
        command.Parameters.AddRange(parameters);

        var result = await command.ExecuteScalarAsync();

        if (result is null || result == DBNull.Value)
        {
            return 0;
        }

        return Convert.ToInt32(result);
    }

    public static async Task<string?> ExecuteScalarStringAsync(
        SqlConnection connection,
        string sql,
        params SqlParameter[] parameters)
    {
        await using var command = new SqlCommand(sql, connection);
        command.Parameters.AddRange(parameters);

        var result = await command.ExecuteScalarAsync();

        return result is null || result == DBNull.Value
            ? null
            : Convert.ToString(result);
    }
}
