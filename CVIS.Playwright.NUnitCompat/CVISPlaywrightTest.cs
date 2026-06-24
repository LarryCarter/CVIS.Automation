using Microsoft.Playwright;
using NUnit.Framework;
using CVIS.Playwright.NUnitCompat;

namespace CVIS.Playwright.NUnitCompat;

/// <summary>
/// CVIS equivalent of Microsoft.Playwright.NUnit.PlaywrightTest.
/// Initializes Microsoft.Playwright, resolves BrowserType, sets test-id selector,
/// and exposes Expect helper methods.
/// </summary>
public class CVISPlaywrightTest : CVISWorkerAwareTest
{
    private static readonly Task<IPlaywright> PlaywrightTask =
        Microsoft.Playwright.Playwright.CreateAsync();

    public string BrowserName { get; private set; } = string.Empty;
    public CVISPlaywrightSettings Settings { get; private set; } = null!;
    public IPlaywright Playwright { get; private set; } = null!;
    public IBrowserType BrowserType { get; private set; } = null!;

    [SetUp]
    public async Task CVISPlaywrightSetupAsync()
    {
        Settings = CVISPlaywrightSettingsProvider.Current;

        Playwright = await PlaywrightTask.ConfigureAwait(false);
        BrowserName = Settings.BrowserName;
        BrowserType = Playwright[BrowserName];

        Playwright.Selectors.SetTestIdAttribute(Settings.TestIdAttribute);

        if (Settings.ExpectTimeout.HasValue)
        {
            SetDefaultExpectTimeout(Settings.ExpectTimeout.Value);
        }
    }

    public static void SetDefaultExpectTimeout(float timeout) =>
        Assertions.SetDefaultExpectTimeout(timeout);

    public ILocatorAssertions Expect(ILocator locator) =>
        Assertions.Expect(locator);

    public IPageAssertions Expect(IPage page) =>
        Assertions.Expect(page);

    public IAPIResponseAssertions Expect(IAPIResponse response) =>
        Assertions.Expect(response);

    public ILocatorAssertions Expect(ILocator locator, string message) =>
        Assertions.Expect(locator, message);

    public IPageAssertions Expect(IPage page, string message) =>
        Assertions.Expect(page, message);

    public IAPIResponseAssertions Expect(IAPIResponse response, string message) =>
        Assertions.Expect(response, message);
}
