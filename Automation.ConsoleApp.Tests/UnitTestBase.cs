using System.Text.Json;

namespace Automation.ConsoleApp.Tests;

public class UnitTestBase
{
    public const string CONSTANT_APPSETTINGS_FILE_NAME = "appsettings.json";
    public const string CONSTANT_APPSETTINGS = "appsettings";

    public bool Analysis { get; } = true;

    public static IConfigurationRoot GetConfiguration()
    {
        return new ConfigurationBuilder()
            .SetBasePath(Directory.GetCurrentDirectory())
            .AddJsonFile(CONSTANT_APPSETTINGS_FILE_NAME, optional: false, reloadOnChange: true)
            .AddEnvironmentVariables()
            .Build();
    }

    public static IEnumerable<T> LoadJsonArray<T>(string relativePath)
    {
        var filePath = ResolveJsonPath(relativePath);

        var json = File.ReadAllText(filePath);

        return JsonSerializer.Deserialize<IEnumerable<T>>(
            json,
            new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true
            }) ?? Enumerable.Empty<T>();
    }

    public static string ResolveJsonPath(string relativePath)
    {
        if (Path.IsPathRooted(relativePath) && File.Exists(relativePath))
        {
            return relativePath;
        }

        var normalizedRelativePath = relativePath
            .Replace('/', Path.DirectorySeparatorChar)
            .Replace('\\', Path.DirectorySeparatorChar);

        var current = new DirectoryInfo(Directory.GetCurrentDirectory());

        while (current is not null)
        {
            var candidates = new[]
            {
                Path.Combine(current.FullName, normalizedRelativePath),
                Path.Combine(current.FullName, "Automation.ConsoleApp.Tests", normalizedRelativePath),
                Path.Combine(current.FullName, "Automation.ConsoleApp.Tests", "Integration", "PolicyDrift", "TestData", Path.GetFileName(normalizedRelativePath)),
                Path.Combine(current.FullName, "CVIS.Automation.Tests", "Projects", "PolicyDrift", "TestData", Path.GetFileName(normalizedRelativePath))
            };

            foreach (var candidate in candidates)
            {
                if (File.Exists(candidate))
                {
                    return candidate;
                }
            }

            current = current.Parent;
        }

        throw new FileNotFoundException(
            $"Unable to locate JSON test data file '{relativePath}'. Current directory: {Directory.GetCurrentDirectory()}");
    }
}
