using CVIS.Playwright.NUnitCompat;
namespace CVIS.Playwright.NUnitCompat.Tests.Utilities;

public sealed class EnvironmentVariableScope : IDisposable
{
    private readonly Dictionary<string, string?> _originalValues = new(StringComparer.OrdinalIgnoreCase);

    public EnvironmentVariableScope Set(string name, string? value)
    {
        if (!_originalValues.ContainsKey(name))
        {
            _originalValues[name] = Environment.GetEnvironmentVariable(name);
        }

        Environment.SetEnvironmentVariable(name, value);
        return this;
    }

    public void Dispose()
    {
        foreach (var item in _originalValues)
        {
            Environment.SetEnvironmentVariable(item.Key, item.Value);
        }
    }
}
