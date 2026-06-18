namespace CVIS.Playwright.NUnitCompat.Tests.Contracts;

[TestFixture]
[Category("PlaywrightCompatUnit")]
public sealed class CVISPlaywrightHierarchyContractTests
{
    [Test]
    public void CVISPageTest_ShouldMatchExpectedInheritanceChain()
    {
        typeof(CVISPageTest).IsSubclassOf(typeof(CVISContextTest)).Should().BeTrue();
        typeof(CVISContextTest).IsSubclassOf(typeof(CVISBrowserTest)).Should().BeTrue();
        typeof(CVISBrowserTest).IsSubclassOf(typeof(CVISPlaywrightTest)).Should().BeTrue();
        typeof(CVISPlaywrightTest).IsSubclassOf(typeof(CVISWorkerAwareTest)).Should().BeTrue();
    }

    [Test]
    public void CVISApiTest_ShouldInheritFromPlaywrightTest()
    {
        typeof(CVISApiTest).IsSubclassOf(typeof(CVISPlaywrightTest)).Should().BeTrue();
    }

    [Test]
    public void CVISBrowserTest_ShouldExposeExpectedVirtualExtensionPoints()
    {
        typeof(CVISBrowserTest)
            .GetMethod(nameof(CVISBrowserTest.ConnectOptionsAsync))!
            .IsVirtual
            .Should()
            .BeTrue();

        typeof(CVISBrowserTest)
            .GetMethod(nameof(CVISBrowserTest.LaunchOptionsAsync))!
            .IsVirtual
            .Should()
            .BeTrue();
    }

    [Test]
    public void CVISContextTest_ShouldExposeContextOptionsOverride()
    {
        typeof(CVISContextTest)
            .GetMethod(nameof(CVISContextTest.ContextOptions))!
            .IsVirtual
            .Should()
            .BeTrue();
    }

    [Test]
    public void CVISPlaywrightTest_ShouldExposeExpectHelpers()
    {
        var methodNames = typeof(CVISPlaywrightTest)
            .GetMethods()
            .Where(method => method.Name == "Expect")
            .ToList();

        methodNames.Count.Should().BeGreaterThanOrEqualTo(3);
    }
}
