using CVIS.FunctionalTesting.Base;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Examples;

[TestFixture]
[Category("PolicyDrift")]
[Category("Functional")]
public sealed class PolicyDriftValidationTests : BaseFunctionalTest
{
    [Test]
    public void Policy_RequiredFields_ArePresent()
    {
        var policy = new
        {
            Id = "P001",
            Name = "Test Policy",
            Status = "Active"
        };

        Assert.Multiple(() =>
        {
            Assert.That(policy.Id, Is.Not.Null.And.Not.Empty);
            Assert.That(policy.Name, Is.Not.Null.And.Not.Empty);
            Assert.That(policy.Status, Is.EqualTo("Active"));
        });
    }

    [TestCase("P001", "Active", true)]
    [TestCase("P002", "Inactive", false)]
    [TestCase("P003", "Pending", false)]
    public void Policy_StatusMapping_IsCorrect(string policyId, string status, bool expectedActive)
    {
        var isActive = status == "Active";

        Assert.That(isActive, Is.EqualTo(expectedActive), $"Policy {policyId} active mapping mismatch.");
    }
}
