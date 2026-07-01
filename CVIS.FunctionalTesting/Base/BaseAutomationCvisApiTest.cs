using CVIS.FunctionalTesting.Helpers;
using NUnit.Framework;

namespace CVIS.FunctionalTesting.Base;

/// <summary>
/// Base class for CVIS API automation tests.
/// Provides an ApiClient created from appsettings.test.json.
/// </summary>
[TestFixture]
public abstract class BaseAutomationCvisApiTest : BaseAutomationCvisTest
{
    protected ApiClient ApiClient { get; private set; } = null!;

    [SetUp]
    public virtual void ApiTestSetUp()
    {
        ApiClient = new ApiClient(Config);
        Logger.Info("[API] ApiClient created.");
    }

    [TearDown]
    public virtual void ApiTestTearDown()
    {
        ApiClient?.Dispose();
        Logger.Info("[API] ApiClient disposed.");
    }
}
