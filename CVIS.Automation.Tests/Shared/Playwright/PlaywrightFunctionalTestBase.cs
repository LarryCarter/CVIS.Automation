using Microsoft.Playwright;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Shared.Playwright;

public abstract class PlaywrightFunctionalTestBase
{
    protected IPlaywright PlaywrightRuntime { get; private set; } = null!;

    [SetUp]
    public async Task PlaywrightFunctionalSetupAsync()
    {
        PlaywrightRuntime = await Microsoft.Playwright.Playwright.CreateAsync();
    }

    [TearDown]
    public void PlaywrightFunctionalTearDown()
    {
        PlaywrightRuntime?.Dispose();
    }

    protected async Task ConfirmPlaywrightRuntimeAsync()
    {
        if (PlaywrightRuntime is null)
        {
            Assert.Fail("Playwright runtime was not initialized for this functional regression test.");
        }

        await using var requestContext = await PlaywrightRuntime.APIRequest.NewContextAsync();

        Assert.That(
            requestContext,
            Is.Not.Null,
            "A Playwright APIRequestContext must be created before this test can count as Playwright-backed.");

        await Task.CompletedTask;
    }
}
