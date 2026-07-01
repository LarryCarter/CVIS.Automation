using CVIS.FunctionalTesting.Config;
using CVIS.FunctionalTesting.Reporting;
using NUnit.Framework;

namespace CVIS.FunctionalTesting.Base;

/// <summary>
/// Official root base class for normal CVIS NUnit automation tests.
/// Use this when the test needs CVIS configuration, logging, and lifecycle diagnostics,
/// but does not require API helpers, database helpers, or browser automation.
/// </summary>
[TestFixture]
public abstract class BaseAutomationCvisTest
{
    protected FunctionalTestConfig Config { get; private set; } = null!;
    protected TestLogger Logger { get; private set; } = null!;

    private DateTime _testStartedUtc;

    [OneTimeSetUp]
    public async Task AutomationFixtureSetUpAsync()
    {
        Config = FunctionalTestConfig.Load();
        Logger = new TestLogger(TestContext.CurrentContext.Test.ClassName ?? GetType().Name);
        Logger.Info($"[Fixture] Starting: {TestContext.CurrentContext.Test.ClassName}");

        await OnFixtureSetUpAsync().ConfigureAwait(false);
    }

    [SetUp]
    public async Task AutomationTestSetUpAsync()
    {
        _testStartedUtc = DateTime.UtcNow;
        Logger.Info($"[Test] Starting: {TestContext.CurrentContext.Test.FullName}");

        await OnTestSetUpAsync().ConfigureAwait(false);
    }

    [TearDown]
    public async Task AutomationTestTearDownAsync()
    {
        try
        {
            await OnTestTearDownAsync().ConfigureAwait(false);
        }
        finally
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
    }

    [OneTimeTearDown]
    public async Task AutomationFixtureTearDownAsync()
    {
        try
        {
            await OnFixtureTearDownAsync().ConfigureAwait(false);
        }
        finally
        {
            Logger.Info($"[Fixture] Completed: {TestContext.CurrentContext.Test.ClassName}");
        }
    }

    /// <summary>
    /// Override for specialized one-time fixture setup. Do not add NUnit lifecycle attributes in derived base classes.
    /// </summary>
    protected virtual Task OnFixtureSetUpAsync() => Task.CompletedTask;

    /// <summary>
    /// Override for specialized per-test setup. Do not add NUnit lifecycle attributes in derived base classes.
    /// </summary>
    protected virtual Task OnTestSetUpAsync() => Task.CompletedTask;

    /// <summary>
    /// Override for specialized per-test teardown. Do not add NUnit lifecycle attributes in derived base classes.
    /// </summary>
    protected virtual Task OnTestTearDownAsync() => Task.CompletedTask;

    /// <summary>
    /// Override for specialized one-time fixture teardown. Do not add NUnit lifecycle attributes in derived base classes.
    /// </summary>
    protected virtual Task OnFixtureTearDownAsync() => Task.CompletedTask;
}
