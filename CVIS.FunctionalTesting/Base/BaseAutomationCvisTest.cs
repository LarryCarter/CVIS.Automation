using CVIS.FunctionalTesting.Config;
using CVIS.FunctionalTesting.Reporting;
using NUnit.Framework;

namespace CVIS.FunctionalTesting.Base;

/// <summary>
/// Base class for normal CVIS NUnit automation tests.
/// Use this when the test needs CVIS configuration, logging, and lifecycle diagnostics,
/// but does not require API, database, or browser setup.
/// </summary>
[TestFixture]
public abstract class BaseAutomationCvisTest
{
    protected FunctionalTestConfig Config { get; private set; } = null!;
    protected TestLogger Logger { get; private set; } = null!;

    private DateTime _testStartedUtc;

    [OneTimeSetUp]
    public virtual void AutomationFixtureSetUp()
    {
        Config = FunctionalTestConfig.Load();
        Logger = new TestLogger(TestContext.CurrentContext.Test.ClassName ?? GetType().Name);
        Logger.Info($"[Fixture] Starting: {TestContext.CurrentContext.Test.ClassName}");
    }

    [SetUp]
    public virtual void AutomationTestSetUp()
    {
        _testStartedUtc = DateTime.UtcNow;
        Logger.Info($"[Test] Starting: {TestContext.CurrentContext.Test.FullName}");
    }

    [TearDown]
    public virtual void AutomationTestTearDown()
    {
        var result = TestContext.CurrentContext.Result;
        var duration = DateTime.UtcNow - _testStartedUtc;

        Logger.Info(
            $"[Test] Finished: {TestContext.CurrentContext.Test.FullName} " +
            $"| Outcome: {result.Outcome.Status} " +
            $"| Duration: {duration.TotalMilliseconds:N0}ms");

        TestLifecycleLog.Record(new TestLifecycleEntry
        {
            TestName = TestContext.CurrentContext.Test.FullName,
            FixtureClass = GetType().FullName ?? GetType().Name,
            Outcome = result.Outcome.Status.ToString(),
            Message = result.Message,
            StackTrace = result.StackTrace,
            DurationMs = (long)duration.TotalMilliseconds,
            StartedAt = _testStartedUtc
        });
    }

    [OneTimeTearDown]
    public virtual void AutomationFixtureTearDown()
    {
        Logger.Info($"[Fixture] Completed: {TestContext.CurrentContext.Test.ClassName}");
    }
}
