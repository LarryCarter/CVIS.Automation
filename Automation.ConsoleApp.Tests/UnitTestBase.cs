namespace Automation.ConsoleApp.Tests;

public abstract class UnitTestBase
{
    public const string CONSTANT_APPSETTINGS_FILE_NAME = "appsettings.json";
    public const string CONSTANT_APPSETTINGS = "appsettings";

    protected static IConfigurationRoot GetConfiguration()
    {
        return new ConfigurationBuilder()
            .SetBasePath(AppContext.BaseDirectory)
            .AddJsonFile(CONSTANT_APPSETTINGS_FILE_NAME, optional: false, reloadOnChange: true)
            .AddEnvironmentVariables()
            .Build();
    }

    protected static IReadOnlyList<T> LoadJsonArray<T>(params string[] relativePathParts)
    {
        var path = Path.Combine(new[] { AppContext.BaseDirectory }.Concat(relativePathParts).ToArray());

        if (!File.Exists(path))
        {
            throw new FileNotFoundException($"Required test data file was not found: {path}", path);
        }

        var json = File.ReadAllText(path);
        var options = new JsonSerializerOptions(JsonSerializerDefaults.Web)
        {
            PropertyNameCaseInsensitive = true
        };

        return JsonSerializer.Deserialize<IReadOnlyList<T>>(json, options) ?? Array.Empty<T>();
    }
}
