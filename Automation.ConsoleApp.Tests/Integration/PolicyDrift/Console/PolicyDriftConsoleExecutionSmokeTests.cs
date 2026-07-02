using FluentAssertions;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Console;

public sealed class PolicyDriftConsoleExecutionSmokeTests : UnitTestBase
{
    [Fact]
    [Trait("PolicyDrift", "true")]
    [Trait("ConsoleRegression", "true")]
    public void PolicyDriftConsole_ShouldHaveSmokeTestHarness()
    {
        Analysis.Should().BeTrue();
    }
}
