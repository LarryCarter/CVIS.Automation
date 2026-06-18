r"""
CVIS RDEL Update Script
Package: CVIS Playwright NUnitCompat Test Project

Purpose:
    Creates a separate NUnit test project for CVIS.Playwright.NUnitCompat tests.
    This keeps the compatibility-layer unit tests isolated from CVIS.Automation.Tests.

Runs from solution root:
    C:\Users\larry\source\repos\CVIS.Automation
"""

from __future__ import annotations

from pathlib import Path
import shutil
import subprocess


SOLUTION_ROOT = Path.cwd()
COMPAT_ROOT = SOLUTION_ROOT / "CVIS.Playwright.NUnitCompat"
COMPAT_CSPROJ = COMPAT_ROOT / "CVIS.Playwright.NUnitCompat.csproj"

TEST_ROOT = SOLUTION_ROOT / "CVIS.Playwright.NUnitCompat.Tests"
TEST_CSPROJ = TEST_ROOT / "CVIS.Playwright.NUnitCompat.Tests.csproj"

OLD_TESTS = SOLUTION_ROOT / "CVIS.Automation.Tests" / "Shared" / "PlaywrightCompatTests"


def require_layout() -> None:
    if not COMPAT_CSPROJ.exists():
        raise RuntimeError(
            "Cannot find CVIS.Playwright.NUnitCompat. "
            "Run the CVIS Playwright NUnitCompat feature-layer package first."
        )

    TEST_ROOT.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def remove_old_embedded_tests() -> None:
    # These tests belong in the new dedicated test project, not CVIS.Automation.Tests.
    if OLD_TESTS.exists():
        shutil.rmtree(OLD_TESTS)


def write_test_project() -> None:
    write_text(
        TEST_CSPROJ,
        """<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <IsPackable>false</IsPackable>
    <IsTestProject>true</IsTestProject>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="FluentAssertions" Version="8.10.0" />
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.8.0" />
    <PackageReference Include="NUnit" Version="3.13.3" />
    <PackageReference Include="NUnit3TestAdapter" Version="4.2.1" />
    <PackageReference Include="NUnit.Analyzers" Version="3.6.1" />
    <PackageReference Include="coverlet.collector" Version="6.0.0" />
  </ItemGroup>

  <ItemGroup>
    <ProjectReference Include="..\\CVIS.Playwright.NUnitCompat\\CVIS.Playwright.NUnitCompat.csproj" />
  </ItemGroup>

</Project>
""",
    )


def write_test_files() -> None:
    write_text(
        TEST_ROOT / "GlobalUsings.cs",
        """global using System;
global using System.Collections.Generic;
global using System.Linq;
global using System.Threading.Tasks;
global using FluentAssertions;
global using NUnit.Framework;
""",
    )

    write_text(
        TEST_ROOT / "Utilities" / "EnvironmentVariableScope.cs",
        """namespace CVIS.Playwright.NUnitCompat.Tests.Utilities;

public sealed class EnvironmentVariableScope : IDisposable
{
    private readonly Dictionary<string, string?> _originalValues = new(StringComparer.OrdinalIgnoreCase);

    public EnvironmentVariableScope Set(string name, string? value)
    {
        if (!_originalValues.ContainsKey(name))
        {
            _originalValues[name] = Environment.GetEnvironmentVariable(name);
        }

        Environment.SetEnvironmentVariable(name, value);
        return this;
    }

    public void Dispose()
    {
        foreach (var item in _originalValues)
        {
            Environment.SetEnvironmentVariable(item.Key, item.Value);
        }
    }
}
""",
    )

    write_text(
        TEST_ROOT / "Utilities" / "LoopbackHttpServer.cs",
        """using System.Net;
using System.Net.Sockets;
using System.Text;

namespace CVIS.Playwright.NUnitCompat.Tests.Utilities;

public sealed class LoopbackHttpServer : IAsyncDisposable
{
    private readonly TcpListener _listener;
    private readonly CancellationTokenSource _cancellationTokenSource = new();
    private readonly Task _acceptLoop;

    public Uri Uri { get; }

    public LoopbackHttpServer()
    {
        _listener = new TcpListener(IPAddress.Loopback, 0);
        _listener.Start();

        var port = ((IPEndPoint)_listener.LocalEndpoint).Port;
        Uri = new Uri($"http://127.0.0.1:{port}/");

        _acceptLoop = Task.Run(AcceptLoopAsync);
    }

    private async Task AcceptLoopAsync()
    {
        while (!_cancellationTokenSource.IsCancellationRequested)
        {
            try
            {
                using var client = await _listener.AcceptTcpClientAsync(_cancellationTokenSource.Token);
                await using var stream = client.GetStream();

                var buffer = new byte[4096];
                _ = await stream.ReadAsync(buffer, _cancellationTokenSource.Token);

                var body = "CVIS loopback ok";
                var bodyBytes = Encoding.UTF8.GetBytes(body);

                var headerBuilder = new StringBuilder();
                headerBuilder.Append("HTTP/1.1 200 OK\\r\\n");
                headerBuilder.Append("Content-Type: text/plain; charset=utf-8\\r\\n");
                headerBuilder.Append("Content-Length: ");
                headerBuilder.Append(bodyBytes.Length);
                headerBuilder.Append("\\r\\n");
                headerBuilder.Append("Connection: close\\r\\n");
                headerBuilder.Append("\\r\\n");

                var headerBytes = Encoding.ASCII.GetBytes(headerBuilder.ToString());

                await stream.WriteAsync(headerBytes, _cancellationTokenSource.Token);
                await stream.WriteAsync(bodyBytes, _cancellationTokenSource.Token);
            }
            catch (OperationCanceledException)
            {
                break;
            }
            catch
            {
                // Keep the server alive for remaining tests.
            }
        }
    }

    public async ValueTask DisposeAsync()
    {
        _cancellationTokenSource.Cancel();
        _listener.Stop();

        try
        {
            await _acceptLoop;
        }
        catch
        {
            // Ignore shutdown exceptions.
        }

        _cancellationTokenSource.Dispose();
    }
}
""",
    )

    write_text(
        TEST_ROOT / "Settings" / "CVISPlaywrightSettingsProviderTests.cs",
        """using CVIS.Playwright.NUnitCompat.Tests.Utilities;

namespace CVIS.Playwright.NUnitCompat.Tests.Settings;

[TestFixture]
[Category("PlaywrightCompatUnit")]
public sealed class CVISPlaywrightSettingsProviderTests
{
    [Test]
    public void FromEnvironment_WhenUnset_ShouldDefaultToChromiumHeadless()
    {
        using var env = new EnvironmentVariableScope()
            .Set("BROWSER", null)
            .Set("HEADED", null)
            .Set("PWDEBUG", null)
            .Set("EXPECT_TIMEOUT", null)
            .Set("SLOW_MO", null)
            .Set("TEST_ID_ATTRIBUTE", null);

        var settings = CVISPlaywrightSettingsProvider.FromEnvironment();

        settings.BrowserName.Should().Be("chromium");
        settings.Headed.Should().BeFalse();
        settings.Headless.Should().BeTrue();
        settings.ExpectTimeout.Should().BeNull();
        settings.SlowMo.Should().BeNull();
        settings.TestIdAttribute.Should().Be("data-testid");
    }

    [TestCase("chromium")]
    [TestCase("firefox")]
    [TestCase("webkit")]
    public void FromEnvironment_WhenBrowserSet_ShouldAcceptSupportedBrowser(string browser)
    {
        using var env = new EnvironmentVariableScope()
            .Set("BROWSER", browser);

        var settings = CVISPlaywrightSettingsProvider.FromEnvironment();

        settings.BrowserName.Should().Be(browser);
    }

    [Test]
    public void FromEnvironment_WhenInvalidBrowserSet_ShouldThrow()
    {
        using var env = new EnvironmentVariableScope()
            .Set("BROWSER", "bad-browser");

        Action action = () => CVISPlaywrightSettingsProvider.FromEnvironment();

        action.Should().Throw<InvalidOperationException>()
            .WithMessage("*bad-browser*");
    }

    [TestCase("1")]
    [TestCase("true")]
    [TestCase("yes")]
    public void FromEnvironment_WhenHeadedSet_ShouldSetHeadedAndDisableHeadless(string value)
    {
        using var env = new EnvironmentVariableScope()
            .Set("HEADED", value);

        var settings = CVISPlaywrightSettingsProvider.FromEnvironment();

        settings.Headed.Should().BeTrue();
        settings.Headless.Should().BeFalse();
    }

    [Test]
    public void FromEnvironment_WhenPwDebugSet_ShouldSetHeadedAndDisableHeadless()
    {
        using var env = new EnvironmentVariableScope()
            .Set("PWDEBUG", "1");

        var settings = CVISPlaywrightSettingsProvider.FromEnvironment();

        settings.Headed.Should().BeTrue();
        settings.Headless.Should().BeFalse();
    }

    [Test]
    public void FromEnvironment_WhenTimeoutSlowMoAndTestIdSet_ShouldMapValues()
    {
        using var env = new EnvironmentVariableScope()
            .Set("EXPECT_TIMEOUT", "2500")
            .Set("SLOW_MO", "100")
            .Set("TEST_ID_ATTRIBUTE", "data-cvis-id");

        var settings = CVISPlaywrightSettingsProvider.FromEnvironment();

        settings.ExpectTimeout.Should().Be(2500);
        settings.SlowMo.Should().Be(100);
        settings.TestIdAttribute.Should().Be("data-cvis-id");
    }

    [Test]
    public void ToLaunchOptions_ShouldMapHeadlessAndSlowMo()
    {
        var settings = new CVISPlaywrightSettings
        {
            Headless = false,
            SlowMo = 75
        };

        var options = CVISPlaywrightSettingsProvider.ToLaunchOptions(settings);

        options.Headless.Should().BeFalse();
        options.SlowMo.Should().Be(75);
    }
}
""",
    )

    write_text(
        TEST_ROOT / "Contracts" / "CVISPlaywrightHierarchyContractTests.cs",
        """namespace CVIS.Playwright.NUnitCompat.Tests.Contracts;

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
""",
    )

    write_text(
        TEST_ROOT / "Runtime" / "CVISPlaywrightTestRuntimeTests.cs",
        """namespace CVIS.Playwright.NUnitCompat.Tests.Runtime;

[TestFixture]
[Category("PlaywrightCompatUnit")]
public sealed class CVISPlaywrightTestRuntimeTests : CVISPlaywrightTest
{
    [Test]
    public void Setup_ShouldInitializePlaywrightBrowserNameAndBrowserType()
    {
        Playwright.Should().NotBeNull();
        BrowserName.Should().BeOneOf("chromium", "firefox", "webkit");
        BrowserType.Should().NotBeNull();
        Settings.Should().NotBeNull();
    }
}
""",
    )

    write_text(
        TEST_ROOT / "Runtime" / "CVISApiTestRuntimeTests.cs",
        """using CVIS.Playwright.NUnitCompat.Tests.Utilities;

namespace CVIS.Playwright.NUnitCompat.Tests.Runtime;

[TestFixture]
[Category("PlaywrightCompatUnit")]
public sealed class CVISApiTestRuntimeTests : CVISApiTest
{
    [Test]
    public void Setup_ShouldCreateDefaultApiContext()
    {
        ApiContext.Should().NotBeNull();
    }

    [Test]
    public async Task NewApiRequestContextAsync_ShouldCallLoopbackServerThroughPlaywright()
    {
        await using var server = new LoopbackHttpServer();

        var context = await NewApiRequestContextAsync(server.Uri.ToString());
        var response = await context.GetAsync("/");

        response.Ok.Should().BeTrue();

        var body = await response.TextAsync();
        body.Should().Contain("CVIS loopback ok");
    }

    [Test]
    public async Task NewApiContextAsync_ShouldCallLoopbackServerThroughPlaywright()
    {
        await using var server = new LoopbackHttpServer();

        var context = await NewApiContextAsync(server.Uri.ToString());
        var response = await context.GetAsync("/");

        response.Ok.Should().BeTrue();

        var body = await response.TextAsync();
        body.Should().Contain("CVIS loopback ok");
    }
}
""",
    )

    write_text(
        TEST_ROOT / "Browser" / "CVISContextOptionsTests.cs",
        """using Microsoft.Playwright;

namespace CVIS.Playwright.NUnitCompat.Tests.Browser;

[TestFixture]
[Category("PlaywrightCompatUnit")]
public sealed class CVISContextOptionsTests
{
    [Test]
    public void ContextOptions_ShouldDefaultToEnglishLightColorScheme()
    {
        var test = new CVISContextTest();

        var options = test.ContextOptions();

        options.Locale.Should().Be("en-US");
        options.ColorScheme.Should().Be(ColorScheme.Light);
    }
}
""",
    )

    write_text(
        TEST_ROOT / "Browser" / "CVISBrowserLaunchOptionsTests.cs",
        """namespace CVIS.Playwright.NUnitCompat.Tests.Browser;

[TestFixture]
[Category("PlaywrightCompatUnit")]
public sealed class CVISBrowserLaunchOptionsTests
{
    private sealed class TestBrowserTest : CVISBrowserTest
    {
    }

    [Test]
    public async Task DefaultConnectOptionsAsync_ShouldReturnNull()
    {
        var test = new TestBrowserTest();

        var options = await test.ConnectOptionsAsync();

        options.Should().BeNull();
    }

    [Test]
    public async Task DefaultLaunchOptionsAsync_ShouldReturnNull()
    {
        var test = new TestBrowserTest();

        var options = await test.LaunchOptionsAsync();

        options.Should().BeNull();
    }
}
""",
    )


def add_test_project_to_solution() -> None:
    sln_files = list(SOLUTION_ROOT.glob("*.sln"))

    if not sln_files:
        return

    sln = sln_files[0]

    subprocess.run(
        ["dotnet", "sln", str(sln), "add", str(TEST_CSPROJ)],
        cwd=SOLUTION_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def main() -> None:
    require_layout()
    remove_old_embedded_tests()
    write_test_project()
    write_test_files()
    add_test_project_to_solution()

    print("Created CVIS.Playwright.NUnitCompat.Tests.")
    print("Removed embedded compatibility tests from CVIS.Automation.Tests if present.")


if __name__ == "__main__":
    main()
