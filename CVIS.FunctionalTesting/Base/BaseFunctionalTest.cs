using CVIS.FunctionalTesting.Config;
using CVIS.FunctionalTesting.Reporting;
using NUnit.Framework;
using NUnit.Framework.Interfaces;

namespace CVIS.FunctionalTesting.Base;

/// <summary>
/// Base class for ALL non-Playwright functional tests.
/// Inherit from this for: API tests, PolicyDrift tests, DB tests, config/logic tests.
/// No Playwright dependency.
/// </summary>
[TestFixture]
public abstract class BaseFunctionalTest
{
    protected FunctionalTestConfig Config { get; private set; } = null!;
    protected TestLogger Logger { get; private set; } = null!;

    private DateTime _testStartTime;

    [OneTimeSetUp]
    public virtual void FixtureSetUp()
    {
        Config = FunctionalTestConfig.Load();
        Logger = new TestLogger(TestContext.CurrentContext.Test.ClassName ?? nameof(BaseFunctionalTest));
        Logger.Info($"[Fixture] Starting: {TestContext.CurrentContext.Test.ClassName}");
    }

    [SetUp]
    public virtual void TestSetUp()
    {
        _testStartTime = DateTime.UtcNow;
        Logger?.Info($"[Test] Starting: {TestContext.CurrentContext.Test.Name}");
    }

    [TearDown]
    public virtual void TestTearDown()
    {
        var result = TestContext.CurrentContext.Result;
        var duration = DateTime.UtcNow - _testStartTime;

        Logger?.Info(
            $"[Test] Finished: {TestContext.CurrentContext.Test.Name} " +
            $"| Outcome: {result.Outcome.Status} " +
            $"| Duration: {duration.TotalSeconds:F2}s");

        // Records to cpn-lifecycle-report only.
        // The authoritative cpn-report.html is generated after dotnet test
        // by CVIS.Playwright.Reporting.Tool reading TRX and NUnit XML files.
        TestLifecycleLog.Record(new TestLifecycleEntry
        {
            TestName = TestContext.CurrentContext.Test.FullName,
            Outcome = result.Outcome.Status.ToString(),
            DurationMs = (long)duration.TotalMilliseconds,
            Message = result.Message,
            StackTrace = result.StackTrace,
            FixtureClass = GetType().FullName ?? string.Empty,
            StartedAt = _testStartTime
        });
    }

    [OneTimeTearDown]
    public virtual void FixtureTearDown()
    {
        Logger?.Info($"[Fixture] Completed: {TestContext.CurrentContext.Test.ClassName}");
    }
}
