using CVIS.Playwright.Automation.Shared.Helpers;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Projects.LegacySustainment.Workflows;

[TestFixture]
[Category("LegacySustainment")]
[Category("WorkflowRegression")]
public sealed class LegacySustainmentWorkflowPlaceholderTests
{
    private const string ProjectName = "LegacySustainment";

    [Test]
    public void LegacySustainmentAutomationProject_ShouldBeConfigurable()
    {
        var config = TestConfig.Load();
        var project = config.GetProject(ProjectName);

        if (!project.Enabled)
        {
            Assert.Ignore("LegacySustainment automation tests are disabled in appsettings.test.json.");
        }

        Assert.Pass("LegacySustainment automation project configuration is available.");
    }
}
