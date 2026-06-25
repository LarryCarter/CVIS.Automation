using NUnit.Framework;

namespace CVIS.FunctionalTesting.Reporting;

/// <summary>
/// Lightweight logger. Writes to NUnit's TestContext.Out so output
/// appears in VS Test Explorer, dotnet test console, and NUnit XML.
/// </summary>
public sealed class TestLogger
{
    private readonly string _context;

    public TestLogger(string context)
    {
        _context = context ?? "Unknown";
    }

    public void Info(string message) => Write("INFO", message);
    public void Warn(string message) => Write("WARN", message);
    public void Error(string message) => Write("ERROR", message);
    public void Debug(string message) => Write("DEBUG", message);

    private void Write(string level, string message) =>
        TestContext.Out.WriteLine($"[{DateTime.UtcNow:HH:mm:ss.fff}] [{level}] [{_context}] {message}");
}
