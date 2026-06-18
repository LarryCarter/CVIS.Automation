r"""
CVIS RDEL Update Script
Package: CVIS Playwright NUnitCompat Feature Layer

Purpose:
    Adds a separate CVIS.Playwright.NUnitCompat class library that recreates
    the major Microsoft.Playwright.NUnit convenience features without replacing
    existing PolicyDrift tests yet.

Runs from solution root:
    C:\Users\larry\source\repos\CVIS.Automation
"""

from __future__ import annotations

from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET


SOLUTION_ROOT = Path.cwd()
TEST_PROJECT_ROOT = SOLUTION_ROOT / "CVIS.Automation.Tests"
TEST_CSPROJ = TEST_PROJECT_ROOT / "CVIS.Automation.Tests.csproj"

COMPAT_ROOT = SOLUTION_ROOT / "CVIS.Playwright.NUnitCompat"
COMPAT_CSPROJ = COMPAT_ROOT / "CVIS.Playwright.NUnitCompat.csproj"

TEST_COMPAT_ROOT = TEST_PROJECT_ROOT / "Shared" / "PlaywrightCompatTests"


def require_layout() -> None:
    if not TEST_PROJECT_ROOT.exists():
        raise RuntimeError("Cannot find CVIS.Automation.Tests. Run from the CVIS.Automation solution root.")

    if not TEST_CSPROJ.exists():
        raise RuntimeError(f"Cannot find test project file: {TEST_CSPROJ}")

    COMPAT_ROOT.mkdir(parents=True, exist_ok=True)
    TEST_COMPAT_ROOT.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_project_file() -> None:
    write_text(
        COMPAT_CSPROJ,
        """<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <IsPackable>false</IsPackable>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.Playwright" Version="1.60.0" />
    <PackageReference Include="NUnit" Version="3.13.3" />
  </ItemGroup>

</Project>
""",
    )


def add_project_reference_to_tests() -> None:
    tree = ET.parse(TEST_CSPROJ)
    root = tree.getroot()

    relative_reference = r"..\CVIS.Playwright.NUnitCompat\CVIS.Playwright.NUnitCompat.csproj"

    for project_reference in root.findall(".//ProjectReference"):
        if project_reference.attrib.get("Include", "").lower() == relative_reference.lower():
            tree.write(TEST_CSPROJ, encoding="utf-8", xml_declaration=True)
            return

    item_group = ET.SubElement(root, "ItemGroup")
    project_reference = ET.SubElement(item_group, "ProjectReference")
    project_reference.set("Include", relative_reference)

    indent_xml(root)
    tree.write(TEST_CSPROJ, encoding="utf-8", xml_declaration=True)


def indent_xml(elem: ET.Element, level: int = 0) -> None:
    space = "\n" + level * "  "

    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = space + "  "

        for child in elem:
            indent_xml(child, level + 1)

        if not elem[-1].tail or not elem[-1].tail.strip():
            elem[-1].tail = space

    if level and (not elem.tail or not elem.tail.strip()):
        elem.tail = space


def try_add_project_to_solution() -> None:
    sln_files = list(SOLUTION_ROOT.glob("*.sln"))

    if not sln_files:
        return

    sln = sln_files[0]

    subprocess.run(
        ["dotnet", "sln", str(sln), "add", str(COMPAT_CSPROJ)],
        cwd=SOLUTION_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def write_worker_aware_test() -> None:
    write_text(
        COMPAT_ROOT / "CVISWorkerAwareTest.cs",
        """using NUnit.Framework;
using NUnit.Framework.Interfaces;

namespace CVIS.Playwright.NUnitCompat;

/// <summary>
/// Minimal CVIS equivalent of the worker-aware foundation used by Playwright.NUnit.
/// Provides test outcome helpers for teardown behavior.
/// </summary>
public abstract class CVISWorkerAwareTest
{
    protected bool TestOk()
    {
        return TestContext.CurrentContext.Result.Outcome.Status == TestStatus.Passed;
    }

    protected string TestName =>
        TestContext.CurrentContext.Test.Name;

    protected string WorkerId =>
        Environment.GetEnvironmentVariable("NUNIT_WORKER_ID")
        ?? Environment.GetEnvironmentVariable("TEST_WORKER_INDEX")
        ?? "0";
}
""",
    )


def write_settings_provider() -> None:
    write_text(
        COMPAT_ROOT / "CVISPlaywrightSettingsProvider.cs",
        """using Microsoft.Playwright;

namespace CVIS.Playwright.NUnitCompat;

public sealed record CVISPlaywrightSettings
{
    public string BrowserName { get; init; } = "chromium";
    public bool Headed { get; init; }
    public bool Headless { get; init; } = true;
    public float? ExpectTimeout { get; init; }
    public float? SlowMo { get; init; }
    public string TestIdAttribute { get; init; } = "data-testid";
}

public static class CVISPlaywrightSettingsProvider
{
    private static readonly HashSet<string> ValidBrowsers =
        new(StringComparer.OrdinalIgnoreCase)
        {
            "chromium",
            "firefox",
            "webkit"
        };

    public static CVISPlaywrightSettings Current => FromEnvironment();

    public static CVISPlaywrightSettings FromEnvironment()
    {
        var browserName = Environment.GetEnvironmentVariable("BROWSER");

        if (string.IsNullOrWhiteSpace(browserName))
        {
            browserName = "chromium";
        }

        browserName = browserName.Trim().ToLowerInvariant();

        if (!ValidBrowsers.Contains(browserName))
        {
            throw new InvalidOperationException(
                $"Invalid BROWSER value '{browserName}'. Expected chromium, firefox, or webkit.");
        }

        var headed = ReadBoolean("HEADED") || ReadBoolean("PWDEBUG");
        var expectTimeout = ReadNullableFloat("EXPECT_TIMEOUT");
        var slowMo = ReadNullableFloat("SLOW_MO");

        var testIdAttribute = Environment.GetEnvironmentVariable("TEST_ID_ATTRIBUTE");

        if (string.IsNullOrWhiteSpace(testIdAttribute))
        {
            testIdAttribute = "data-testid";
        }

        return new CVISPlaywrightSettings
        {
            BrowserName = browserName,
            Headed = headed,
            Headless = !headed,
            ExpectTimeout = expectTimeout,
            SlowMo = slowMo,
            TestIdAttribute = testIdAttribute
        };
    }

    public static BrowserTypeLaunchOptions ToLaunchOptions(CVISPlaywrightSettings settings)
    {
        return new BrowserTypeLaunchOptions
        {
            Headless = settings.Headless,
            SlowMo = settings.SlowMo
        };
    }

    private static bool ReadBoolean(string name)
    {
        var value = Environment.GetEnvironmentVariable(name);

        if (string.IsNullOrWhiteSpace(value))
        {
            return false;
        }

        return value.Equals("1", StringComparison.OrdinalIgnoreCase)
            || value.Equals("true", StringComparison.OrdinalIgnoreCase)
            || value.Equals("yes", StringComparison.OrdinalIgnoreCase);
    }

    private static float? ReadNullableFloat(string name)
    {
        var value = Environment.GetEnvironmentVariable(name);

        if (string.IsNullOrWhiteSpace(value))
        {
            return null;
        }

        if (float.TryParse(value, out var parsed))
        {
            return parsed;
        }

        return null;
    }
}
""",
    )


def write_playwright_test() -> None:
    write_text(
        COMPAT_ROOT / "CVISPlaywrightTest.cs",
        """using Microsoft.Playwright;
using NUnit.Framework;

namespace CVIS.Playwright.NUnitCompat;

/// <summary>
/// CVIS equivalent of Microsoft.Playwright.NUnit.PlaywrightTest.
/// Initializes Microsoft.Playwright, resolves BrowserType, sets test-id selector,
/// and exposes Expect helper methods.
/// </summary>
public class CVISPlaywrightTest : CVISWorkerAwareTest
{
    private static readonly Task<IPlaywright> PlaywrightTask =
        Microsoft.Playwright.Playwright.CreateAsync();

    public string BrowserName { get; private set; } = string.Empty;
    public CVISPlaywrightSettings Settings { get; private set; } = null!;
    public IPlaywright Playwright { get; private set; } = null!;
    public IBrowserType BrowserType { get; private set; } = null!;

    [SetUp]
    public async Task CVISPlaywrightSetupAsync()
    {
        Settings = CVISPlaywrightSettingsProvider.Current;

        Playwright = await PlaywrightTask.ConfigureAwait(false);
        BrowserName = Settings.BrowserName;
        BrowserType = Playwright[BrowserName];

        Playwright.Selectors.SetTestIdAttribute(Settings.TestIdAttribute);

        if (Settings.ExpectTimeout.HasValue)
        {
            SetDefaultExpectTimeout(Settings.ExpectTimeout.Value);
        }
    }

    public static void SetDefaultExpectTimeout(float timeout) =>
        Assertions.SetDefaultExpectTimeout(timeout);

    public ILocatorAssertions Expect(ILocator locator) =>
        Assertions.Expect(locator);

    public IPageAssertions Expect(IPage page) =>
        Assertions.Expect(page);

    public IAPIResponseAssertions Expect(IAPIResponse response) =>
        Assertions.Expect(response);

    public ILocatorAssertions Expect(ILocator locator, string message) =>
        Assertions.Expect(locator, message);

    public IPageAssertions Expect(IPage page, string message) =>
        Assertions.Expect(page, message);

    public IAPIResponseAssertions Expect(IAPIResponse response, string message) =>
        Assertions.Expect(response, message);
}
""",
    )


def write_browser_service() -> None:
    write_text(
        COMPAT_ROOT / "CVISBrowserService.cs",
        """using System.Collections.Concurrent;
using Microsoft.Playwright;

namespace CVIS.Playwright.NUnitCompat;

public sealed class CVISBrowserService
{
    private static readonly ConcurrentDictionary<string, Lazy<Task<CVISBrowserService>>> Services = new();

    private CVISBrowserService(IBrowser browser)
    {
        Browser = browser;
    }

    public IBrowser Browser { get; }

    public static Task<CVISBrowserService> RegisterAsync(
        IBrowserType browserType,
        (string Endpoint, BrowserTypeConnectOptions? Options)? connectOptions,
        BrowserTypeLaunchOptions? launchOptions)
    {
        var key = CreateKey(browserType.Name, connectOptions, launchOptions);

        return Services.GetOrAdd(
            key,
            _ => new Lazy<Task<CVISBrowserService>>(
                () => CreateAsync(browserType, connectOptions, launchOptions))).Value;
    }

    public static async Task CloseAllAsync()
    {
        foreach (var service in Services.Values)
        {
            var resolved = await service.Value.ConfigureAwait(false);
            await resolved.Browser.CloseAsync().ConfigureAwait(false);
        }

        Services.Clear();
    }

    private static async Task<CVISBrowserService> CreateAsync(
        IBrowserType browserType,
        (string Endpoint, BrowserTypeConnectOptions? Options)? connectOptions,
        BrowserTypeLaunchOptions? launchOptions)
    {
        IBrowser browser;

        if (connectOptions.HasValue)
        {
            browser = await browserType.ConnectAsync(
                connectOptions.Value.Endpoint,
                connectOptions.Value.Options).ConfigureAwait(false);
        }
        else
        {
            browser = await browserType.LaunchAsync(launchOptions).ConfigureAwait(false);
        }

        return new CVISBrowserService(browser);
    }

    private static string CreateKey(
        string browserName,
        (string Endpoint, BrowserTypeConnectOptions? Options)? connectOptions,
        BrowserTypeLaunchOptions? launchOptions)
    {
        var connectKey = connectOptions.HasValue
            ? connectOptions.Value.Endpoint
            : "launch";

        var headedKey = launchOptions?.Headless?.ToString() ?? "default";
        var slowMoKey = launchOptions?.SlowMo?.ToString() ?? "none";

        return $"{browserName}|{connectKey}|headless:{headedKey}|slowmo:{slowMoKey}";
    }
}
""",
    )


def write_browser_test() -> None:
    write_text(
        COMPAT_ROOT / "CVISBrowserTest.cs",
        """using Microsoft.Playwright;
using NUnit.Framework;

namespace CVIS.Playwright.NUnitCompat;

/// <summary>
/// CVIS equivalent of Microsoft.Playwright.NUnit.BrowserTest.
/// Provides Browser, NewContext, LaunchOptionsAsync, and ConnectOptionsAsync.
/// </summary>
public class CVISBrowserTest : CVISPlaywrightTest
{
    private readonly List<IBrowserContext> _contexts = new();

    public IBrowser Browser { get; private set; } = null!;

    public async Task<IBrowserContext> NewContext(BrowserNewContextOptions? options = null)
    {
        var context = await Browser.NewContextAsync(options).ConfigureAwait(false);
        _contexts.Add(context);
        return context;
    }

    [SetUp]
    public async Task CVISBrowserSetupAsync()
    {
        var launchOptions = await LaunchOptionsAsync().ConfigureAwait(false)
            ?? CVISPlaywrightSettingsProvider.ToLaunchOptions(Settings);

        var service = await CVISBrowserService.RegisterAsync(
            BrowserType,
            await ConnectOptionsAsync().ConfigureAwait(false),
            launchOptions).ConfigureAwait(false);

        Browser = service.Browser;
    }

    [TearDown]
    public async Task CVISBrowserTearDownAsync()
    {
        if (TestOk())
        {
            foreach (var context in _contexts)
            {
                await context.CloseAsync().ConfigureAwait(false);
            }
        }

        _contexts.Clear();
        Browser = null!;
    }

    public virtual Task<(string Endpoint, BrowserTypeConnectOptions? Options)?> ConnectOptionsAsync() =>
        Task.FromResult<(string Endpoint, BrowserTypeConnectOptions? Options)?>(null);

    public virtual Task<BrowserTypeLaunchOptions?> LaunchOptionsAsync() =>
        Task.FromResult<BrowserTypeLaunchOptions?>(null);
}
""",
    )


def write_context_test() -> None:
    write_text(
        COMPAT_ROOT / "CVISContextTest.cs",
        """using Microsoft.Playwright;
using NUnit.Framework;

namespace CVIS.Playwright.NUnitCompat;

/// <summary>
/// CVIS equivalent of Microsoft.Playwright.NUnit.ContextTest.
/// Creates one BrowserContext per test.
/// </summary>
public class CVISContextTest : CVISBrowserTest
{
    public IBrowserContext Context { get; private set; } = null!;

    [SetUp]
    public async Task CVISContextSetupAsync()
    {
        Context = await NewContext(ContextOptions()).ConfigureAwait(false);
    }

    public virtual BrowserNewContextOptions ContextOptions()
    {
        return new BrowserNewContextOptions
        {
            Locale = "en-US",
            ColorScheme = ColorScheme.Light
        };
    }
}
""",
    )


def write_page_test() -> None:
    write_text(
        COMPAT_ROOT / "CVISPageTest.cs",
        """using Microsoft.Playwright;
using NUnit.Framework;

namespace CVIS.Playwright.NUnitCompat;

/// <summary>
/// CVIS equivalent of Microsoft.Playwright.NUnit.PageTest.
/// Creates one Page per test.
/// </summary>
public class CVISPageTest : CVISContextTest
{
    public IPage Page { get; private set; } = null!;

    [SetUp]
    public async Task CVISPageSetupAsync()
    {
        Page = await Context.NewPageAsync().ConfigureAwait(false);
    }
}
""",
    )


def write_api_test() -> None:
    write_text(
        COMPAT_ROOT / "CVISApiTest.cs",
        """using Microsoft.Playwright;
using NUnit.Framework;

namespace CVIS.Playwright.NUnitCompat;

/// <summary>
/// CVIS API-focused extension for console/API/database regression projects.
/// Provides APIRequestContext creation without requiring browser/page setup.
/// </summary>
public class CVISApiTest : CVISPlaywrightTest
{
    private readonly List<IAPIRequestContext> _apiContexts = new();

    public async Task<IAPIRequestContext> NewApiContextAsync(
        string? baseUrl = null,
        IDictionary<string, string>? headers = null,
        bool ignoreHttpsErrors = true)
    {
        var context = await Playwright.APIRequest.NewContextAsync(
            new APIRequestNewContextOptions
            {
                BaseURL = baseUrl,
                ExtraHTTPHeaders = headers,
                IgnoreHTTPSErrors = ignoreHttpsErrors
            }).ConfigureAwait(false);

        _apiContexts.Add(context);
        return context;
    }

    [TearDown]
    public async Task CVISApiTearDownAsync()
    {
        foreach (var context in _apiContexts)
        {
            await context.DisposeAsync().ConfigureAwait(false);
        }

        _apiContexts.Clear();
    }
}
""",
    )


def write_test_loopback_server() -> None:
    write_text(
        TEST_COMPAT_ROOT / "LoopbackHttpServer.cs",
        """using System.Net;
using System.Net.Sockets;
using System.Text;

namespace CVIS.Automation.Tests.Shared.PlaywrightCompatTests;

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


def write_compat_tests() -> None:
    write_text(
        TEST_COMPAT_ROOT / "CVISPlaywrightSettingsProviderTests.cs",
        """using CVIS.Playwright.NUnitCompat;
using FluentAssertions;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Shared.PlaywrightCompatTests;

[TestFixture]
[Category("PlaywrightCompatibility")]
public sealed class CVISPlaywrightSettingsProviderTests
{
    [Test]
    public void FromEnvironment_ShouldDefaultToChromiumHeadless()
    {
        Environment.SetEnvironmentVariable("BROWSER", null);
        Environment.SetEnvironmentVariable("HEADED", null);
        Environment.SetEnvironmentVariable("PWDEBUG", null);

        var settings = CVISPlaywrightSettingsProvider.FromEnvironment();

        settings.BrowserName.Should().Be("chromium");
        settings.Headless.Should().BeTrue();
        settings.TestIdAttribute.Should().Be("data-testid");
    }

    [Test]
    public void FromEnvironment_ShouldRespectBrowserAndHeaded()
    {
        Environment.SetEnvironmentVariable("BROWSER", "firefox");
        Environment.SetEnvironmentVariable("HEADED", "1");

        var settings = CVISPlaywrightSettingsProvider.FromEnvironment();

        settings.BrowserName.Should().Be("firefox");
        settings.Headed.Should().BeTrue();
        settings.Headless.Should().BeFalse();

        Environment.SetEnvironmentVariable("BROWSER", null);
        Environment.SetEnvironmentVariable("HEADED", null);
    }

    [Test]
    public void FromEnvironment_ShouldRejectInvalidBrowser()
    {
        Environment.SetEnvironmentVariable("BROWSER", "invalid-browser");

        Action action = () => CVISPlaywrightSettingsProvider.FromEnvironment();

        action.Should().Throw<InvalidOperationException>();

        Environment.SetEnvironmentVariable("BROWSER", null);
    }
}
""",
    )

    write_text(
        TEST_COMPAT_ROOT / "CVISPlaywrightTestCompatibilityTests.cs",
        """using CVIS.Playwright.NUnitCompat;
using FluentAssertions;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Shared.PlaywrightCompatTests;

[TestFixture]
[Category("PlaywrightCompatibility")]
public sealed class CVISPlaywrightTestCompatibilityTests : CVISPlaywrightTest
{
    [Test]
    public void PlaywrightSetup_ShouldInitializeRuntimeAndBrowserType()
    {
        Playwright.Should().NotBeNull();
        BrowserType.Should().NotBeNull();
        BrowserName.Should().BeOneOf("chromium", "firefox", "webkit");
    }
}
""",
    )

    write_text(
        TEST_COMPAT_ROOT / "CVISApiTestCompatibilityTests.cs",
        """using CVIS.Playwright.NUnitCompat;
using FluentAssertions;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Shared.PlaywrightCompatTests;

[TestFixture]
[Category("PlaywrightCompatibility")]
public sealed class CVISApiTestCompatibilityTests : CVISApiTest
{
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
        TEST_COMPAT_ROOT / "CVISBrowserHierarchyContractTests.cs",
        """using CVIS.Playwright.NUnitCompat;
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
""",
    )


def main() -> None:
    require_layout()
    write_project_file()
    add_project_reference_to_tests()
    try_add_project_to_solution()

    write_worker_aware_test()
    write_settings_provider()
    write_playwright_test()
    write_browser_service()
    write_browser_test()
    write_context_test()
    write_page_test()
    write_api_test()

    write_test_loopback_server()
    write_compat_tests()

    print("Added CVIS.Playwright.NUnitCompat project and compatibility tests.")
    print("No PolicyDrift tests were replaced.")


if __name__ == "__main__":
    main()
