namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Matrix;

internal static class UnitTestData
{
    public static IReadOnlyList<T> LoadJsonArray<T>(params string[] relativePathParts)
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
