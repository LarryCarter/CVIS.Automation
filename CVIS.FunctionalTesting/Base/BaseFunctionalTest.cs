namespace CVIS.FunctionalTesting.Base;

/// <summary>
/// Legacy compatibility alias for the old non-browser functional test base.
/// New tests should inherit BaseAutomationCvisTest instead.
/// </summary>
[Obsolete("Use BaseAutomationCvisTest. BaseFunctionalTest remains only as a temporary compatibility alias.")]
public abstract class BaseFunctionalTest : BaseAutomationCvisTest
{
}
