namespace CVIS.Playwright.NUnitCompat.Base;

/// <summary>
/// Legacy compatibility alias for the old CVIS Playwright page base.
/// New CVIS automation tests should inherit BaseAutomationCvisPlaywrightPageTabTest instead.
/// </summary>
[Obsolete("Use BaseAutomationCvisPlaywrightPageTabTest. CVISPageTest remains only as a temporary compatibility alias.")]
public abstract class CVISPageTest : BaseAutomationCvisPlaywrightPageTabTest
{
}
