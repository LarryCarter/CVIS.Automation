using System.Text.Json;

namespace CVIS.Playwright.Automation.Shared.Helpers;

public static class TestDataLoader
{
    public static IReadOnlyList<T> LoadJsonArray<T>(string relativePath)
    {
        var path = Path.Combine(AppContext.BaseDirectory, relativePath);

        if (!File.Exists(path))
        {
            throw new FileNotFoundException($"Missing test data file: {path}");
        }

        var json = File.ReadAllText(path);

        return JsonSerializer.Deserialize<List<T>>(
            json,
            new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true
            }) ?? new List<T>();
    }
}
