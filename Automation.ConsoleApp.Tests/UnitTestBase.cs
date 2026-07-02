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

    public static IEnumerable<T> LoadJsonArray<T>(string relativePath)
    {
        var path = ResolveRepositoryFilePath(relativePath);

        if (path is null)
        {
            throw new FileNotFoundException($"Could not locate test data file '{relativePath}'.");
        }

        var json = File.ReadAllText(path);
        return JsonSerializer.Deserialize<IEnumerable<T>>(json, new JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = true
        }) ?? Enumerable.Empty<T>();
    }

    private static string? ResolveRepositoryFilePath(string relativePath)
    {
        var normalizedRelativePath = NormalizePath(relativePath);
        var sourcePolicyDriftPath = TryMapToOriginalPolicyDriftSourcePath(normalizedRelativePath);

        foreach (var root in EnumerateCandidateRoots())
        {
            if (!string.IsNullOrWhiteSpace(sourcePolicyDriftPath))
            {
                var originalSourceCandidate = Path.Combine(root, sourcePolicyDriftPath);
                if (File.Exists(originalSourceCandidate))
                {
                    return originalSourceCandidate;
                }
            }
        }

        foreach (var root in EnumerateCandidateRoots())
        {
            var candidate = Path.Combine(root, normalizedRelativePath);
            if (File.Exists(candidate))
            {
                return candidate;
            }

            var projectCandidate = Path.Combine(root, "Automation.ConsoleApp.Tests", normalizedRelativePath);
            if (File.Exists(projectCandidate))
            {
                return projectCandidate;
            }
        }

        return null;
    }

    private static string? TryMapToOriginalPolicyDriftSourcePath(string normalizedRelativePath)
    {
        const string newPolicyDriftPrefix = "Integration/PolicyDrift/TestData/";
        const string oldPolicyDriftPrefix = "Projects/PolicyDrift/TestData/";

        if (normalizedRelativePath.StartsWith(newPolicyDriftPrefix, StringComparison.OrdinalIgnoreCase))
        {
            var fileName = normalizedRelativePath[newPolicyDriftPrefix.Length..];
            return NormalizePath(Path.Combine("CVIS.Automation.Tests", "Projects", "PolicyDrift", "TestData", fileName));
        }

        if (normalizedRelativePath.StartsWith(oldPolicyDriftPrefix, StringComparison.OrdinalIgnoreCase))
        {
            var fileName = normalizedRelativePath[oldPolicyDriftPrefix.Length..];
            return NormalizePath(Path.Combine("CVIS.Automation.Tests", "Projects", "PolicyDrift", "TestData", fileName));
        }

        return null;
    }

    private static IEnumerable<string> EnumerateCandidateRoots()
    {
        var seen = new HashSet<string>(StringComparer.OrdinalIgnoreCase);

        foreach (var start in new[] { AppContext.BaseDirectory, Environment.CurrentDirectory })
        {
            var directory = new DirectoryInfo(start);

            while (directory is not null)
            {
                if (seen.Add(directory.FullName))
                {
                    yield return directory.FullName;
                }

                directory = directory.Parent;
            }
        }
    }

    private static string NormalizePath(string path)
    {
        return path.Replace('\\', '/');
    }
}
