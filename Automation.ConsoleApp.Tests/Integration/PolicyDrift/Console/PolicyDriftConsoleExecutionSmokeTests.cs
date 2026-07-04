using FluentAssertions;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Console;

public sealed class PolicyDriftConsoleExecutionSmokeTests : UnitTestBase
{
    [Fact]
[Trait("PolicyDrift", "true")]
    public void PolicyDriftConsole_PolicyDrift_ShouldHaveSmokeTestHarness()
    {
        Analysis.Should().BeTrue();
    }

    [Fact]
[Trait("ConsoleRegression", "true")]
    public void PolicyDriftConsole_ConsoleRegression_ShouldHaveSmokeTestHarness()
    {
        Analysis.Should().BeTrue();
    }
}
