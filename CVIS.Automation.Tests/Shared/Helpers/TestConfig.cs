using System.Text.Json;

namespace CVIS.Automation.Tests.Shared.Helpers;

public sealed class TestConfig
{
    public string EnvironmentName { get; set; } = "QA";
    public Dictionary<string, ProjectAutomationConfig> Projects { get; set; } = new(StringComparer.OrdinalIgnoreCase);
    public TestSettingsConfig TestSettings { get; set; } = new();

    public static TestConfig Load()
    {
        var path = Path.Combine(AppContext.BaseDirectory, "appsettings.test.json");

        if (!File.Exists(path))
        {
            throw new FileNotFoundException($"Missing test config file: {path}");
        }

        var json = File.ReadAllText(path);

        return JsonSerializer.Deserialize<TestConfig>(
            json,
            new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true
            }) ?? throw new InvalidOperationException("Unable to deserialize appsettings.test.json.");
    }

    public ProjectAutomationConfig GetProject(string projectName)
    {
        if (!Projects.TryGetValue(projectName, out var project))
        {
            throw new InvalidOperationException($"Project configuration was not found: {projectName}");
        }

        return project;
    }
}

public sealed class ProjectAutomationConfig
{
    public bool Enabled { get; set; }
    public CyberArkConfig CyberArk { get; set; } = new();
    public JobApiConfig JobApi { get; set; } = new();
    public DatabaseConfig Database { get; set; } = new();
    public ConsoleAppsConfig ConsoleApps { get; set; } = new();
}

public sealed class CyberArkConfig
{
    public string BaseUrl { get; set; } = string.Empty;
    public string Token { get; set; } = string.Empty;
    public bool UseTokenFromEnvironmentVariable { get; set; } = true;
    public string TokenEnvironmentVariableName { get; set; } = string.Empty;

    public string ResolveToken()
    {
        if (!UseTokenFromEnvironmentVariable)
        {
            return Token;
        }

        if (string.IsNullOrWhiteSpace(TokenEnvironmentVariableName))
        {
            return string.Empty;
        }

        return Environment.GetEnvironmentVariable(TokenEnvironmentVariableName) ?? string.Empty;
    }
}

public sealed class JobApiConfig
{
    public string BaseUrl { get; set; } = string.Empty;
    public bool UseJobApi { get; set; }
}

public sealed class DatabaseConfig
{
    public string ConnectionString { get; set; } = string.Empty;
}

public sealed class ConsoleAppsConfig
{
    public string WorkingDirectory { get; set; } = string.Empty;
    public string ZipDownloaderExePath { get; set; } = string.Empty;
    public string PolicyDriftExePath { get; set; } = string.Empty;
    public string ReportExePath { get; set; } = string.Empty;
}

public sealed class TestSettingsConfig
{
    public bool RunApiTests { get; set; }
    public bool RunDatabaseTests { get; set; } = true;
    public bool RunConsoleExecutionTests { get; set; }
    public bool RunJobTriggerTests { get; set; }
    public int DefaultTimeoutSeconds { get; set; } = 120;
}
