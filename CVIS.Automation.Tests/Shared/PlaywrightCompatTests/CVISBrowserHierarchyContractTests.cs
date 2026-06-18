using CVIS.Playwright.NUnitCompat;
using FluentAssertions;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Shared.PlaywrightCompatTests;

[TestFixture]
[Category("PlaywrightCompatibility")]
public sealed class CVISBrowserHierarchyContractTests
{
    [Test]
    public void PageTest_ShouldInheritExpectedHierarchy()
    {
        typeof(CVISPageTest).IsSubclassOf(typeof(CVISContextTest)).Should().BeTrue();
        typeof(CVISContextTest).IsSubclassOf(typeof(CVISBrowserTest)).Should().BeTrue();
        typeof(CVISBrowserTest).IsSubclassOf(typeof(CVISPlaywrightTest)).Should().BeTrue();
        typeof(CVISPlaywrightTest).IsSubclassOf(typeof(CVISWorkerAwareTest)).Should().BeTrue();
    }

    [Test]
    public void ApiTest_ShouldInheritPlaywrightTest()
    {
        typeof(CVISApiTest).IsSubclassOf(typeof(CVISPlaywrightTest)).Should().BeTrue();
    }
}
