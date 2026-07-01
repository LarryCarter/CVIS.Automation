using System.Text.Json;

namespace CVIS.FunctionalTesting.Config;

/// <summary>
/// Shared configuration for CVIS automation tests.
/// This configuration is intentionally not domain-specific.
/// Domains such as PolicyDrift, Unity, and LegacySustainment should consume capabilities
/// through API, database, browser, or normal automation base classes.
/// </summary>
public sealed class FunctionalTestConfig
{
    private static readonly object Gate = new();
    private static FunctionalTestConfig? _instance;

    public string BaseUrl { get; set; } = "http://localhost";
    public string ApiBaseUrl { get; set; } = "http://localhost/api";
    public string DatabaseConnection { get; set; } = string.Empty;
    public string Environment { get; set; } = "Test";
    public int DefaultTimeoutMilliseconds { get; set; } = 30_000;
    public bool VerboseLogging { get; set; }

    public PolicyDriftConfig PolicyDrift { get; set; } = new();
    public ApiTestConfig Api { get; set; } = new();

    public static FunctionalTestConfig Load(string? configPath = null)
    {
        lock (Gate)
        {
            if (_instance is not null)
            {
                return _instance;
            }

            configPath ??= FindConfigFile();

            if (configPath is null || !File.Exists(configPath))
            {
                _instance = new FunctionalTestConfig();
                return _instance;
            }

            try
            {
                var json = File.ReadAllText(configPath);
                var options = new JsonSerializerOptions
                {
                    PropertyNameCaseInsensitive = true
                };

                _instance = JsonSerializer.Deserialize<FunctionalTestConfig>(json, options)
                            ?? new FunctionalTestConfig();
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[CVIS Config] Failed to load {configPath}: {ex.Message}");
                _instance = new FunctionalTestConfig();
            }

            return _instance;
        }
    }

    internal static void ResetForTests()
    {
        lock (Gate)
        {
            _instance = null;
        }
    }

    private static string? FindConfigFile()
    {
        var directory = AppContext.BaseDirectory;

        for (var index = 0; index < 8; index++)
        {
            var candidate = Path.Combine(directory, "appsettings.test.json");

            if (File.Exists(candidate))
            {
                return candidate;
            }

            var parent = Directory.GetParent(directory);

            if (parent is null)
            {
                return null;
            }

            directory = parent.FullName;
        }

        return null;
    }
}

public sealed class PolicyDriftConfig
{
    public string DataPath { get; set; } = "TestData/PolicyDrift";
    public bool RunSlowTests { get; set; }
}

public sealed class ApiTestConfig
{
    public string AuthToken { get; set; } = string.Empty;
    public int RetryCount { get; set; } = 3;
}
