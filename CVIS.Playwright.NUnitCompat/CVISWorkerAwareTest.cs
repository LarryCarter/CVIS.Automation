using NUnit.Framework;
using NUnit.Framework.Interfaces;

namespace CVIS.Playwright.NUnitCompat;

/// <summary>
/// Minimal CVIS equivalent of the worker-aware foundation used by Playwright.NUnit.
/// Provides test outcome helpers for teardown behavior.
/// </summary>
public abstract class CVISWorkerAwareTest
{
    protected bool TestOk()
    {
        return TestContext.CurrentContext.Result.Outcome.Status == TestStatus.Passed;
    }

    protected string TestName =>
        TestContext.CurrentContext.Test.Name;

    protected string WorkerId =>
        Environment.GetEnvironmentVariable("NUNIT_WORKER_ID")
        ?? Environment.GetEnvironmentVariable("TEST_WORKER_INDEX")
        ?? "0";
}
