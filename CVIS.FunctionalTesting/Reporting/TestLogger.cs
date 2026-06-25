namespace CVIS.FunctionalTesting.Reporting;

public sealed class TestLogger
{
    private readonly string _scope;

    public TestLogger(string scope)
    {
        _scope = scope;
    }

    public void Info(string message)
    {
        Write("INFO", message);
    }

    public void Warning(string message)
    {
        Write("WARN", message);
    }

    public void Error(string message)
    {
        Write("ERROR", message);
    }

    private void Write(string level, string message)
    {
        Console.WriteLine($"[{DateTimeOffset.UtcNow:O}] [{level}] [{_scope}] {message}");
    }
}
