using CVIS.FunctionalTesting.Config;
using CVIS.FunctionalTesting.Reporting;
using NUnit.Framework;

namespace CVIS.FunctionalTesting.Base;

/// <summary>
/// Base class for non-browser functional NUnit tests.
/// Use this for PolicyDrift, API, config, file, database, and service tests.
/// This class has no Playwright dependency.
/// </summary>
[TestFixture]
public abstract class BaseFunctionalTest
{
    private DateTimeOffset _testStartedUtc;

    protected FunctionalTestConfig Config { get; private set; } = null!;
    protected TestLogger Logger { get; private set; } = null!;

    [OneTimeSetUp]
    public virtual void FunctionalFixtureSetUp()
    {
        Config = FunctionalTestConfig.Load();
        Logger = new TestLogger(TestContext.CurrentContext.Test.ClassName ?? GetType().FullName ?? GetType().Name);
        Logger.Info($"[Fixture] Starting {TestContext.CurrentContext.Test.ClassName}");
    }

    [SetUp]
    public virtual void FunctionalTestSetUp()
    {
        _testStartedUtc = DateTimeOffset.UtcNow;
        Logger.Info($"[Test] Starting {TestContext.CurrentContext.Test.FullName}");
    }

    [TearDown]
    public virtual void FunctionalTestTearDown()
    {
        var result = TestContext.CurrentContext.Result;
        var duration = DateTimeOffset.UtcNow - _testStartedUtc;

        Logger.Info(
            $"[Test] Finished {TestContext.CurrentContext.Test.FullName}; " +
            $"Outcome={result.Outcome.Status}; Duration={duration.TotalMilliseconds:N0}ms");

        TestLifecycleLog.Record(new TestLifecycleEntry
        {
            TestName = TestContext.CurrentContext.Test.FullName,
            FixtureClass = GetType().FullName ?? GetType().Name,
            Outcome = result.Outcome.Status.ToString(),
            Message = result.Message,
            StackTrace = result.StackTrace,
            DurationMilliseconds = duration.TotalMilliseconds,
            StartedUtc = _testStartedUtc
        });
    }

    [OneTimeTearDown]
    public virtual void FunctionalFixtureTearDown()
    {
        Logger.Info($"[Fixture] Completed {TestContext.CurrentContext.Test.ClassName}");
    }
}
