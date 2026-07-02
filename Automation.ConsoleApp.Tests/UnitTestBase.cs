using Microsoft.Extensions.Configuration;
using System.Text.Json;

namespace Automation.ConsoleApp.Tests;

public class UnitTestBase
{
    public const string CONSTANT_APPSETTINGS_FILE_NAME = "appsettings.json";
    public const string CONSTANT_APPSETTINGS = "appsettings";

    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        PropertyNameCaseInsensitive = true,
        ReadCommentHandling = JsonCommentHandling.Skip,
        AllowTrailingCommas = true
    };

    public bool Analysis { get; } = true;

    public static IConfigurationRoot GetConfiguration()
    {
        return new ConfigurationBuilder()
            .SetBasePath(ResolveProjectRoot())
            .AddJsonFile(CONSTANT_APPSETTINGS_FILE_NAME, optional: false, reloadOnChange: true)
            .AddEnvironmentVariables()
            .Build();
    }

    public static IReadOnlyList<T> LoadJsonArray<T>(string relativePath)
    {
        var resolvedPath = ResolveDataFile(relativePath);
        var json = File.ReadAllText(resolvedPath);
        var values = JsonSerializer.Deserialize<List<T>>(json, JsonOptions);

        return values ?? [];
    }

    public static string ResolveDataFile(string relativePath)
    {
        var normalizedRelativePath = relativePath
            .Replace('/', Path.DirectorySeparatorChar)
            .Replace('\\', Path.DirectorySeparatorChar);

        foreach (var root in CandidateRoots())
        {
            var directPath = Path.Combine(root, normalizedRelativePath);
            if (File.Exists(directPath))
            {
                return directPath;
            }

            var xunitPolicyDriftPath = Path.Combine(
                root,
                "Automation.ConsoleApp.Tests",
                "Integration",
                "PolicyDrift",
                "TestData",
                Path.GetFileName(normalizedRelativePath));

            if (File.Exists(xunitPolicyDriftPath))
            {
                return xunitPolicyDriftPath;
            }

            var sourcePolicyDriftPath = Path.Combine(
                root,
                "CVIS.Automation.Tests",
                "Projects",
                "PolicyDrift",
                "TestData",
                Path.GetFileName(normalizedRelativePath));

            if (File.Exists(sourcePolicyDriftPath))
            {
                return sourcePolicyDriftPath;
            }
        }

        throw new FileNotFoundException(
            $"Could not resolve test data file '{relativePath}'. Searched current directory, app base directory, Automation.ConsoleApp.Tests/Integration/PolicyDrift/TestData, and CVIS.Automation.Tests/Projects/PolicyDrift/TestData.");
    }

    private static string ResolveProjectRoot()
    {
        foreach (var root in CandidateRoots())
        {
            var projectRoot = Path.Combine(root, "Automation.ConsoleApp.Tests");
            if (File.Exists(Path.Combine(projectRoot, CONSTANT_APPSETTINGS_FILE_NAME)))
            {
                return projectRoot;
            }

            if (File.Exists(Path.Combine(root, CONSTANT_APPSETTINGS_FILE_NAME)))
            {
                return root;
            }
        }

        return Directory.GetCurrentDirectory();
    }

    private static IEnumerable<string> CandidateRoots()
    {
        var seeds = new[]
        {
            Directory.GetCurrentDirectory(),
            AppContext.BaseDirectory
        };

        var seen = new HashSet<string>(StringComparer.OrdinalIgnoreCase);

        foreach (var seed in seeds.Where(static s => !string.IsNullOrWhiteSpace(s)))
        {
            var directory = new DirectoryInfo(seed);

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
}
