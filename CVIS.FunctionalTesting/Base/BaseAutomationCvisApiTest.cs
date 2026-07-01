using CVIS.FunctionalTesting.Helpers;

namespace CVIS.FunctionalTesting.Base;

/// <summary>
/// Official base class for CVIS API automation tests.
/// Inherit from this when the test needs ApiClient and API configuration.
/// </summary>
public abstract class BaseAutomationCvisApiTest : BaseAutomationCvisTest
{
    protected ApiClient ApiClient { get; private set; } = null!;

    protected override async Task OnTestSetUpAsync()
    {
        await base.OnTestSetUpAsync().ConfigureAwait(false);

        ApiClient = new ApiClient(Config);
        Logger.Info("[API] ApiClient created.");
    }

    protected override async Task OnTestTearDownAsync()
    {
        try
        {
            ApiClient?.Dispose();
            Logger.Info("[API] ApiClient disposed.");
        }
        finally
        {
            await base.OnTestTearDownAsync().ConfigureAwait(false);
        }
    }
}
