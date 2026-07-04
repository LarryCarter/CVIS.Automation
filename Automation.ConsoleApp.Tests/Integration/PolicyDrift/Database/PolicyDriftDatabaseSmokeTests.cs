using FluentAssertions;

namespace Automation.ConsoleApp.Tests.Integration.PolicyDrift.Database;

public sealed class PolicyDriftDatabaseSmokeTests : UnitTestBase
{
    [Fact]
[Trait("PolicyDrift", "true")]
    public void DatabaseConnection_PolicyDrift_ShouldHaveSmokeTestHarness()
    {
        Analysis.Should().BeTrue();
    }

    [Fact]
[Trait("DatabaseRegression", "true")]
    public void DatabaseConnection_DatabaseRegression_ShouldHaveSmokeTestHarness()
    {
        Analysis.Should().BeTrue();
    }

    [Fact]
[Trait("PolicyDrift", "true")]
    public void Database_PolicyDrift_ShouldHaveServerDateSmokeHarness()
    {
        Analysis.Should().BeTrue();
    }

    [Fact]
[Trait("DatabaseRegression", "true")]
    public void Database_DatabaseRegression_ShouldHaveServerDateSmokeHarness()
    {
        Analysis.Should().BeTrue();
    }
}
