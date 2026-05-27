using System.Text;
using System.Text.Json;

namespace CVIS.Automation.Tests.Shared.Reporting;

public static class RegressionReportWriter
{
    private static readonly SemaphoreSlim Gate = new(1, 1);

    public static string ReportDirectory =>
        Path.Combine(AppContext.BaseDirectory, "TestReports");

    public static string JsonLinesReportPath =>
        Path.Combine(ReportDirectory, "CVIS-Automation-Regression-Report.jsonl");

    public static string CsvReportPath =>
        Path.Combine(ReportDirectory, "CVIS-Automation-Regression-Report.csv");

    public static async Task WriteAsync(RegressionReportEntry entry)
    {
        Directory.CreateDirectory(ReportDirectory);

        await Gate.WaitAsync();

        try
        {
            await WriteJsonLineAsync(entry);
            await WriteCsvLineAsync(entry);
        }
        finally
        {
            Gate.Release();
        }
    }

    private static async Task WriteJsonLineAsync(RegressionReportEntry entry)
    {
        var json = JsonSerializer.Serialize(
            entry,
            new JsonSerializerOptions
            {
                WriteIndented = false
            });

        await File.AppendAllTextAsync(
            JsonLinesReportPath,
            json + Environment.NewLine,
            Encoding.UTF8);
    }

    private static async Task WriteCsvLineAsync(RegressionReportEntry entry)
    {
        var fileExists = File.Exists(CsvReportPath);

        await using var stream = new FileStream(
            CsvReportPath,
            FileMode.Append,
            FileAccess.Write,
            FileShare.ReadWrite);

        await using var writer = new StreamWriter(stream, Encoding.UTF8);

        if (!fileExists)
        {
            await writer.WriteLineAsync(
                "TimestampUtc,Project,Family,ScenarioName,ScenarioType,ExpectedBehavior,ExpectedFinalStatus,Status,UsesPlaywright,Details");
        }

        await writer.WriteLineAsync(string.Join(
            ",",
            Escape(entry.TimestampUtc.ToString("O")),
            Escape(entry.Project),
            Escape(entry.Family),
            Escape(entry.ScenarioName),
            Escape(entry.ScenarioType),
            Escape(entry.ExpectedBehavior),
            Escape(entry.ExpectedFinalStatus),
            Escape(entry.Status),
            Escape(entry.UsesPlaywright.ToString()),
            Escape(entry.Details)));
    }

    private static string Escape(string value)
    {
        var safe = value
            .Replace(""", """")
            .Replace("\r", " ")
            .Replace("\n", " ");

        return $""{safe}"";
    }
}
