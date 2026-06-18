using Microsoft.Playwright;
using NUnit.Framework;

namespace CVIS.Playwright.NUnitCompat;

/// <summary>
/// CVIS API-focused extension for console/API/database regression projects.
/// Provides APIRequestContext creation without requiring browser/page setup.
/// </summary>
public class CVISApiTest : CVISPlaywrightTest
{
    private readonly List<IAPIRequestContext> _apiContexts = new();

    public async Task<IAPIRequestContext> NewApiContextAsync(
        string? baseUrl = null,
        IDictionary<string, string>? headers = null,
        bool ignoreHttpsErrors = true)
    {
        var context = await Playwright.APIRequest.NewContextAsync(
            new APIRequestNewContextOptions
            {
                BaseURL = baseUrl,
                ExtraHTTPHeaders = headers,
                IgnoreHTTPSErrors = ignoreHttpsErrors
            }).ConfigureAwait(false);

        _apiContexts.Add(context);
        return context;
    }

    [TearDown]
    public async Task CVISApiTearDownAsync()
    {
        foreach (var context in _apiContexts)
        {
            await context.DisposeAsync().ConfigureAwait(false);
        }

        _apiContexts.Clear();
    }
}
