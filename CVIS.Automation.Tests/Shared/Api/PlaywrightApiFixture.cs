using CVIS.Automation.Tests.Shared.Helpers;
using Microsoft.Playwright;

namespace CVIS.Automation.Tests.Shared.Api;

public abstract class PlaywrightApiFixture
{
    protected TestConfig Config { get; private set; } = null!;
    protected IPlaywright Playwright { get; private set; } = null!;

    [SetUp]
    public async Task ApiFixtureSetup()
    {
        Config = TestConfig.Load();
        Playwright = await Microsoft.Playwright.Playwright.CreateAsync();
    }

    [TearDown]
    public void ApiFixtureTeardown()
    {
        Playwright?.Dispose();
    }

    protected async Task<IAPIRequestContext> CreateApiRequestContextAsync(
        string baseUrl,
        string? bearerToken = null)
    {
        var headers = new Dictionary<string, string>();

        if (!string.IsNullOrWhiteSpace(bearerToken))
        {
            headers["Authorization"] = $"Bearer {bearerToken}";
        }

        return await Playwright.APIRequest.NewContextAsync(new APIRequestNewContextOptions
        {
            BaseURL = baseUrl,
            ExtraHTTPHeaders = headers,
            IgnoreHTTPSErrors = true
        });
    }
}
