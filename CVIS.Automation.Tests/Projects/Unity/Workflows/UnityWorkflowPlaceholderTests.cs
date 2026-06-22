using CVIS.Playwright.Automation.Shared.Helpers;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Projects.Unity.Workflows;

[TestFixture]
[Category("Unity")]
[Category("WorkflowRegression")]
public sealed class UnityWorkflowPlaceholderTests
{
    private const string ProjectName = "Unity";

    [Test]
    public void UnityAutomationProject_ShouldBeConfigurable()
    {
        var config = TestConfig.Load();
        var project = config.GetProject(ProjectName);

        if (!project.Enabled)
        {
            Assert.Ignore("Unity automation tests are disabled in appsettings.test.json.");
        }

        Assert.Pass("Unity automation project configuration is available.");
    }
}
