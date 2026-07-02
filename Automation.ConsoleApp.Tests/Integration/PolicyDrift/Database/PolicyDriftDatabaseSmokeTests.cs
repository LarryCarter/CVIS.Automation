using FluentAssertions;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Database;

public sealed class PolicyDriftDatabaseSmokeTests : UnitTestBase
{
    [Fact]
    [Trait("PolicyDrift", "true")]
    [Trait("DatabaseRegression", "true")]
    public void DatabaseConnection_ShouldHaveSmokeTestHarness()
    {
        Analysis.Should().BeTrue();
    }

    [Fact]
    [Trait("PolicyDrift", "true")]
    [Trait("DatabaseRegression", "true")]
    public void Database_ShouldHaveServerDateSmokeHarness()
    {
        Analysis.Should().BeTrue();
    }
}
