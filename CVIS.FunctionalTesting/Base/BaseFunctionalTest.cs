namespace CVIS.FunctionalTesting.Base;

/// <summary>
/// Legacy compatibility alias.
/// New tests should inherit BaseAutomationCvisTest instead.
/// </summary>
[Obsolete("Use BaseAutomationCvisTest. This alias remains only to avoid breaking existing tests.")]
public abstract class BaseFunctionalTest : BaseAutomationCvisTest
{
}
