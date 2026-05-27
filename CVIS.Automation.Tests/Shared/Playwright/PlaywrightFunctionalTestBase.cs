using CVIS.Automation.Tests.Shared.Reporting;
using Microsoft.Playwright;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Shared.Playwright;

public abstract class PlaywrightFunctionalTestBase
{
    protected IPlaywright PlaywrightRuntime { get; private set; } = null!;
    protected IAPIRequestContext PlaywrightRequestContext { get; private set; } = null!;

    [SetUp]
    public async Task PlaywrightFunctionalSetupAsync()
    {
        PlaywrightRuntime = await Microsoft.Playwright.Playwright.CreateAsync();

        PlaywrightRequestContext = await PlaywrightRuntime.APIRequest.NewContextAsync(
            new APIRequestNewContextOptions
            {
                IgnoreHTTPSErrors = true
            });
    }

    [TearDown]
    public async Task PlaywrightFunctionalTearDownAsync()
    {
        if (PlaywrightRequestContext is not null)
        {
            await PlaywrightRequestContext.DisposeAsync();
        }

        PlaywrightRuntime?.Dispose();
    }

    protected async Task ConfirmPlaywrightRuntimeAsync()
    {
        Assert.That(
            PlaywrightRuntime,
            Is.Not.Null,
            "Playwright runtime must be initialized for this functional regression test.");

        Assert.That(
            PlaywrightRequestContext,
            Is.Not.Null,
            "Playwright APIRequestContext must be initialized for this functional regression test.");

        await Task.CompletedTask;
    }

    protected async Task WriteRegressionReportAsync(
        string project,
        string family,
        string scenarioName,
        string scenarioType,
        string expectedBehavior,
        string expectedFinalStatus,
        RegressionReportStatus status,
        string details)
    {
        await RegressionReportWriter.WriteAsync(
            new RegressionReportEntry
            {
                Project = project,
                Family = family,
                ScenarioName = scenarioName,
                ScenarioType = scenarioType,
                ExpectedBehavior = expectedBehavior,
                ExpectedFinalStatus = expectedFinalStatus,
                Status = status.ToString(),
                Details = details,
                UsesPlaywright = PlaywrightRuntime is not null && PlaywrightRequestContext is not null,
                TimestampUtc = DateTime.UtcNow
            });
    }
}
