using System.Text.Json;

namespace Automation.ConsoleApp.Tests;

public class UnitTestBase
{
    public const string CONSTANT_APPSETTINGS_FILE_NAME = "appsettings.json";

    public static IConfigurationRoot GetConfiguration()
    {
        return new ConfigurationBuilder()
            .SetBasePath(AppContext.BaseDirectory)
            .AddJsonFile(CONSTANT_APPSETTINGS_FILE_NAME, optional: true, reloadOnChange: false)
            .AddEnvironmentVariables()
            .Build();
    }

    protected static bool IsEnabled(IConfiguration configuration, string key, bool defaultValue = false)
    {
        var value = configuration.GetValue<bool?>(key);
        return value ?? defaultValue;
    }

    protected static async Task ConfirmPlaywrightRuntimeAsync()
    {
        await Task.CompletedTask;
    }

    protected static async Task WriteRegressionReportAsync(
        string project,
        string family,
        string scenarioName,
        string scenarioType,
        string expectedBehavior,
        string expectedFinalStatus,
        string status,
        string details)
    {
        project.Should().NotBeNullOrWhiteSpace();
        family.Should().NotBeNullOrWhiteSpace();
        scenarioName.Should().NotBeNullOrWhiteSpace();
        scenarioType.Should().NotBeNullOrWhiteSpace();
        expectedBehavior.Should().NotBeNullOrWhiteSpace();
        expectedFinalStatus.Should().NotBeNullOrWhiteSpace();
        status.Should().NotBeNullOrWhiteSpace();
        details.Should().NotBeNullOrWhiteSpace();

        await Task.CompletedTask;
    }

    protected static IEnumerable<T> LoadJsonArray<T>(string relativePath)
    {
        var candidates = new[]
        {
            Path.Combine(AppContext.BaseDirectory, relativePath),
            Path.Combine(Environment.CurrentDirectory, relativePath),
            Path.Combine(Environment.CurrentDirectory, "Automation.ConsoleApp.Tests", relativePath)
        };

        var path = candidates.FirstOrDefault(File.Exists);
        if (path is null)
        {
            throw new FileNotFoundException($"Could not locate test data file '{relativePath}'. Tried: {string.Join(" | ", candidates)}");
        }

        var json = File.ReadAllText(path);
        return JsonSerializer.Deserialize<IEnumerable<T>>(json, new JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = true
        }) ?? Enumerable.Empty<T>();
    }
}
