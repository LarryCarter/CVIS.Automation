using System.Diagnostics;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Console;

public sealed class PolicyDriftConsoleExecutionSmokeTests : UnitTestBase
{
    private readonly IConfigurationRoot _configuration;

    public PolicyDriftConsoleExecutionSmokeTests()
    {
        _configuration = GetConfiguration();
    }

    [Fact]
    [Trait("PolicyDrift", "true")]
    [Trait("Category", "ConsoleRegression")]
    public async Task PolicyDriftConsole_ShouldRunHelpCommand()
    {
        if (!IsEnabled(_configuration, "PolicyDrift:Enabled") ||
            !IsEnabled(_configuration, "PolicyDrift:RunConsoleExecutionTests"))
        {
            return;
        }

        var executablePath = _configuration["PolicyDrift:ConsoleApps:PolicyDriftExePath"];
        var workingDirectory = _configuration["PolicyDrift:ConsoleApps:WorkingDirectory"] ?? Environment.CurrentDirectory;
        var timeoutSeconds = _configuration.GetValue<int?>("PolicyDrift:TestSettings:DefaultTimeoutSeconds") ?? 30;

        executablePath.Should().NotBeNullOrWhiteSpace();
        File.Exists(executablePath).Should().BeTrue($"console executable should exist at {executablePath}");

        using var process = new Process();
        process.StartInfo = new ProcessStartInfo
        {
            FileName = executablePath!,
            Arguments = "--help",
            WorkingDirectory = workingDirectory,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false,
            CreateNoWindow = true
        };

        process.Start().Should().BeTrue();

        var completed = await Task.Run(() => process.WaitForExit(timeoutSeconds * 1000));
        completed.Should().BeTrue("console command should finish before timeout");

        var output = await process.StandardOutput.ReadToEndAsync();
        process.ExitCode.Should().Be(0);
        output.Should().NotBeNullOrWhiteSpace();
    }
}
