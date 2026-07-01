namespace CVIS.Playwright.NUnitCompat;

/// <summary>
/// Base class for CVIS Playwright browser automation tests.
/// Provides Playwright plus a browser instance.
/// Use this when browser automation is required but the test controls context/page creation manually.
/// </summary>
public abstract class BaseAutomationCvisPlaywrightBrowserTest : CVISBrowserTest
{
}
