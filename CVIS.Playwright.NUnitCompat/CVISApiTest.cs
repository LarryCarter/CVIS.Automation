using Microsoft.Playwright;
using NUnit.Framework;

namespace CVIS.Playwright.NUnitCompat;

public abstract class CVISApiTest : CVISPlaywrightTest
{
    public IAPIRequestContext ApiContext { get; private set; } = null!;

    [SetUp]
    public async Task CVISApiSetupAsync()
    {
        ApiContext = await Playwright.APIRequest.NewContextAsync(ApiRequestOptions()).ConfigureAwait(false);
    }

    [TearDown]
    public async Task CVISApiTearDownAsync()
    {
        if (ApiContext is not null) await ApiContext.DisposeAsync().ConfigureAwait(false);
    }

    public virtual APIRequestNewContextOptions ApiRequestOptions() => new() { IgnoreHTTPSErrors = true };
    public async Task<IAPIRequestContext> NewApiRequestContextAsync(APIRequestNewContextOptions? options = null) => await Playwright.APIRequest.NewContextAsync(options ?? ApiRequestOptions()).ConfigureAwait(false);
}
