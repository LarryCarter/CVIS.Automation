namespace CVIS.Playwright.NUnitCompat.Base;

/// <summary>
/// Legacy compatibility alias for the old CVIS Playwright browser base.
/// New CVIS automation tests should inherit BaseAutomationCvisPlaywrightBrowserTest instead.
/// </summary>
[Obsolete("Use BaseAutomationCvisPlaywrightBrowserTest. CVISPlaywrightTest remains only as a temporary compatibility alias.")]
public abstract class CVISPlaywrightTest : BaseAutomationCvisPlaywrightBrowserTest
{
}
