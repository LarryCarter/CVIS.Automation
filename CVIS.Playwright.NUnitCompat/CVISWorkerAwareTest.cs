using NUnit.Framework;
using NUnit.Framework.Interfaces;

namespace CVIS.Playwright.NUnitCompat;

public abstract class CVISWorkerAwareTest
{
    private DateTimeOffset _cpnReportStartUtc;

    protected bool TestOk()
    {
        return TestContext.CurrentContext.Result.Outcome.Status == TestStatus.Passed;
    }

    protected string TestName => TestContext.CurrentContext.Test.Name;

    protected string WorkerId =>
        Environment.GetEnvironmentVariable("NUNIT_WORKER_ID")
        ?? Environment.GetEnvironmentVariable("TEST_WORKER_INDEX")
        ?? "0";

    [SetUp]
    public void CVISWorkerAwareReportSetup()
    {
        _cpnReportStartUtc = DateTimeOffset.UtcNow;
        CPNReportManager.Initialize();
    }

    [TearDown]
    public void CVISWorkerAwareReportTearDown()
    {
        CPNReportManager.RecordCurrentTest(TestContext.CurrentContext, _cpnReportStartUtc);
    }
}
