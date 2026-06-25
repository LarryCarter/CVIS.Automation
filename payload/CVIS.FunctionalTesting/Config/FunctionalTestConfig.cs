using System.Text.Json;

namespace CVIS.FunctionalTesting.Config;

/// <summary>
/// Loads test configuration from appsettings.test.json.
/// Config controls test BEHAVIOUR only — never test EXECUTION.
/// Use [Ignore] or NUnit categories to skip tests, not config flags.
/// </summary>
public sealed class FunctionalTestConfig
{
    public string BaseUrl { get; set; } = "http://localhost";
    public string ApiBaseUrl { get; set; } = "http://localhost/api";
    public string DatabaseConnection { get; set; } = string.Empty;
    public string Environment { get; set; } = "Test";
    public int DefaultTimeoutMs { get; set; } = 30_000;
    public bool VerboseLogging { get; set; }

    public PolicyDriftConfig PolicyDrift { get; set; } = new();
    public ApiTestConfig Api { get; set; } = new();

    private static FunctionalTestConfig? _instance;
    private static readonly object _lock = new();

    public static FunctionalTestConfig Load(string? configPath = null)
    {
        lock (_lock)
        {
            if (_instance is not null)
                return _instance;

            configPath ??= FindConfigFile();

            if (configPath is null || !File.Exists(configPath))
            {
                _instance = new FunctionalTestConfig();
                return _instance;
            }

            try
            {
                var json = File.ReadAllText(configPath);
                var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
                _instance = JsonSerializer.Deserialize<FunctionalTestConfig>(json, options)
                    ?? new FunctionalTestConfig();
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[CVIS Config] Failed to load config from {configPath}: {ex.Message}");
                _instance = new FunctionalTestConfig();
            }

            return _instance;
        }
    }

    private static string? FindConfigFile()
    {
        var dir = AppContext.BaseDirectory;

        for (var i = 0; i < 6; i++)
        {
            var candidate = Path.Combine(dir, "appsettings.test.json");

            if (File.Exists(candidate))
                return candidate;

            dir = Path.GetDirectoryName(dir) ?? dir;
        }

        return null;
    }

    internal static void Reset()
    {
        lock (_lock)
        {
            _instance = null;
        }
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
