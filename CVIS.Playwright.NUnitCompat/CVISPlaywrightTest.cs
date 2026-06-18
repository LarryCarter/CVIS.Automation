using Microsoft.Playwright;
using NUnit.Framework;

namespace CVIS.Playwright.NUnitCompat;

public abstract class CVISPlaywrightTest
{
    private static readonly Task<IPlaywright> PlaywrightTask = Microsoft.Playwright.Playwright.CreateAsync();

    public string BrowserName { get; private set; } = string.Empty;
    public IPlaywright Playwright { get; private set; } = null!;
    public IBrowserType BrowserType { get; private set; } = null!;

    [SetUp]
    public async Task CVISPlaywrightSetupAsync()
    {
        Playwright = await PlaywrightTask.ConfigureAwait(false);
        BrowserName = CVISPlaywrightSettingsProvider.BrowserName;
        BrowserType = Playwright[BrowserName];
        Playwright.Selectors.SetTestIdAttribute(CVISPlaywrightSettingsProvider.TestIdAttribute);
        var expectTimeout = CVISPlaywrightSettingsProvider.ExpectTimeout;
        if (expectTimeout.HasValue) SetDefaultExpectTimeout(expectTimeout.Value);
    }

    public static void SetDefaultExpectTimeout(float timeout) => Assertions.SetDefaultExpectTimeout(timeout);
    public ILocatorAssertions Expect(ILocator locator) => Assertions.Expect(locator);
    public IPageAssertions Expect(IPage page) => Assertions.Expect(page);
    public IAPIResponseAssertions Expect(IAPIResponse response) => Assertions.Expect(response);
    public ILocatorAssertions Expect(ILocator locator, string message) => Assertions.Expect(locator, message);
    public IPageAssertions Expect(IPage page, string message) => Assertions.Expect(page, message);
    public IAPIResponseAssertions Expect(IAPIResponse response, string message) => Assertions.Expect(response, message);
}
