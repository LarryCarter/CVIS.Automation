using CVIS.Playwright.Automation.Shared.Console;
using CVIS.Playwright.Automation.Shared.Helpers;
using FluentAssertions;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Projects.PolicyDrift.Console;

[TestFixture]
[Category("PolicyDrift")]
[Category("ConsoleRegression")]
public sealed class PolicyDriftConsoleExecutionSmokeTests
{
    private const string ProjectName = "PolicyDrift";
    private TestConfig _config = null!;
    private ConsoleAppRunner _runner = null!;

    [SetUp]
    public void Setup()
    {
        _config = TestConfig.Load();
        _runner = new ConsoleAppRunner();
    }

    [Test]
    public async Task PolicyDriftConsole_ShouldRunHelpCommand()
    {
        var project = _config.GetProject(ProjectName);

        if (!project.Enabled || !_config.TestSettings.RunConsoleExecutionTests)
        {
            Assert.Ignore("PolicyDrift console execution tests are disabled in appsettings.test.json.");
        }

        var result = await _runner.RunAsync(
            executablePath: project.ConsoleApps.PolicyDriftExePath,
            arguments: "--help",
            workingDirectory: project.ConsoleApps.WorkingDirectory,
            timeoutSeconds: _config.TestSettings.DefaultTimeoutSeconds);

        result.ExitCode.Should().Be(0);
        result.StandardOutput.Should().NotBeNullOrWhiteSpace();
    }
}
