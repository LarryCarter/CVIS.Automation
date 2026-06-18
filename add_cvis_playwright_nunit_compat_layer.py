r"""
CVIS RDEL Update Script
Package: CVIS Playwright NUnit Compatibility Layer
"""
from __future__ import annotations
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

SOLUTION_ROOT = Path.cwd()
TEST_PROJECT_ROOT = SOLUTION_ROOT / "CVIS.Automation.Tests"
TEST_CSPROJ = TEST_PROJECT_ROOT / "CVIS.Automation.Tests.csproj"
COMPAT_PROJECT_ROOT = SOLUTION_ROOT / "CVIS.Playwright.NUnitCompat"
COMPAT_CSPROJ = COMPAT_PROJECT_ROOT / "CVIS.Playwright.NUnitCompat.csproj"
TEST_COMPAT_ROOT = TEST_PROJECT_ROOT / "Shared" / "PlaywrightCompatTests"

def require_layout() -> None:
    if not TEST_PROJECT_ROOT.exists():
        raise RuntimeError("Cannot find CVIS.Automation.Tests. Run from solution root.")
    if not TEST_CSPROJ.exists():
        raise RuntimeError(f"Cannot find test project file: {TEST_CSPROJ}")

def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8-sig" if path.suffix.lower() == ".csproj" else "utf-8")

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

def get_package_version(package_name: str, default: str) -> str:
    try:
        tree = ET.parse(TEST_CSPROJ)
        root = tree.getroot()
        for package_ref in root.findall(".//PackageReference"):
            include = package_ref.attrib.get("Include", "")
            if include.lower() == package_name.lower():
                return package_ref.attrib.get("Version", default)
    except Exception:
        pass
    return default

def create_compat_project() -> None:
    nunit_version = get_package_version("NUnit", "3.13.3")
    playwright_version = get_package_version("Microsoft.Playwright", get_package_version("Microsoft.Playwright.NUnit", "1.60.0"))
    write_text(COMPAT_CSPROJ, f"""<Project Sdk=\"Microsoft.NET.Sdk\">

  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <IsPackable>false</IsPackable>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include=\"Microsoft.Playwright\" Version=\"{playwright_version}\" />
    <PackageReference Include=\"NUnit\" Version=\"{nunit_version}\" />
  </ItemGroup>

</Project>
""")

def write_compat_files() -> None:
    write_text(COMPAT_PROJECT_ROOT / "CVISPlaywrightSettingsProvider.cs", """using Microsoft.Playwright;

namespace CVIS.Playwright.NUnitCompat;

public static class CVISPlaywrightSettingsProvider
{
    public static string BrowserName
    {
        get
        {
            var browserFromEnv = Environment.GetEnvironmentVariable("BROWSER")?.ToLowerInvariant();
            if (!string.IsNullOrWhiteSpace(browserFromEnv) && !browserFromEnv.StartsWith("/vscode/"))
            {
                ValidateBrowserName(browserFromEnv, "'BROWSER' environment variable");
                return browserFromEnv;
            }
            var cvisBrowser = Environment.GetEnvironmentVariable("CVIS_PLAYWRIGHT_BROWSER")?.ToLowerInvariant();
            if (!string.IsNullOrWhiteSpace(cvisBrowser))
            {
                ValidateBrowserName(cvisBrowser, "'CVIS_PLAYWRIGHT_BROWSER' environment variable");
                return cvisBrowser;
            }
            return BrowserType.Chromium;
        }
    }

    public static string TestIdAttribute => Environment.GetEnvironmentVariable("CVIS_PLAYWRIGHT_TEST_ID_ATTRIBUTE") ?? "data-testid";

    public static float? ExpectTimeout
    {
        get
        {
            var raw = Environment.GetEnvironmentVariable("CVIS_PLAYWRIGHT_EXPECT_TIMEOUT");
            return float.TryParse(raw, out var timeout) ? timeout : null;
        }
    }

    public static BrowserTypeLaunchOptions LaunchOptions
    {
        get
        {
            var options = new BrowserTypeLaunchOptions();
            if (Environment.GetEnvironmentVariable("HEADED") == "1") options.Headless = false;
            var cvisHeadless = Environment.GetEnvironmentVariable("CVIS_PLAYWRIGHT_HEADLESS");
            if (bool.TryParse(cvisHeadless, out var headless)) options.Headless = headless;
            var channel = Environment.GetEnvironmentVariable("CVIS_PLAYWRIGHT_CHANNEL");
            if (!string.IsNullOrWhiteSpace(channel)) options.Channel = channel;
            return options;
        }
    }

    public static void ValidateBrowserName(string browserName, string source)
    {
        if (browserName is BrowserType.Chromium or BrowserType.Firefox or BrowserType.Webkit) return;
        throw new ArgumentException($"Invalid browser name from {source}. Supported browsers: '{BrowserType.Chromium}', '{BrowserType.Firefox}', and '{BrowserType.Webkit}'. Actual browser: '{browserName}'.");
    }
}
""")

    write_text(COMPAT_PROJECT_ROOT / "CVISPlaywrightTest.cs", """using Microsoft.Playwright;
using NUnit.Framework;

namespace CVIS.Playwright.NUnitCompat;

public abstract class CVISPlaywrightTest
{
    private static readonly Task<IPlaywright> PlaywrightTask = Microsoft.Playwright.Playwright.CreateAsync();

    public string BrowserName { get; private set; } = string.Empty;
    public IPlaywright Playwright { get; private set; } = null!;
    public IBrowserType BrowserType { get; private set; } = null!;

    [SetUp]
    public async Task CVISPlaywrightSetupAsync()
    {
        Playwright = await PlaywrightTask.ConfigureAwait(false);
        BrowserName = CVISPlaywrightSettingsProvider.BrowserName;
        BrowserType = Playwright[BrowserName];
        Playwright.Selectors.SetTestIdAttribute(CVISPlaywrightSettingsProvider.TestIdAttribute);
        var expectTimeout = CVISPlaywrightSettingsProvider.ExpectTimeout;
        if (expectTimeout.HasValue) SetDefaultExpectTimeout(expectTimeout.Value);
    }

    public static void SetDefaultExpectTimeout(float timeout) => Assertions.SetDefaultExpectTimeout(timeout);
    public ILocatorAssertions Expect(ILocator locator) => Assertions.Expect(locator);
    public IPageAssertions Expect(IPage page) => Assertions.Expect(page);
    public IAPIResponseAssertions Expect(IAPIResponse response) => Assertions.Expect(response);
    public ILocatorAssertions Expect(ILocator locator, string message) => Assertions.Expect(locator, message);
    public IPageAssertions Expect(IPage page, string message) => Assertions.Expect(page, message);
    public IAPIResponseAssertions Expect(IAPIResponse response, string message) => Assertions.Expect(response, message);
}
""")

    write_text(COMPAT_PROJECT_ROOT / "CVISBrowserService.cs", """using System.Collections.Concurrent;
using Microsoft.Playwright;

namespace CVIS.Playwright.NUnitCompat;

public sealed class CVISBrowserService
{
    private static readonly ConcurrentDictionary<string, Lazy<Task<IBrowser>>> Browsers = new();

    public static Task<IBrowser> GetOrLaunchAsync(IBrowserType browserType, BrowserTypeLaunchOptions launchOptions)
    {
        var key = CreateKey(browserType.Name, launchOptions);
        var lazy = Browsers.GetOrAdd(key, _ => new Lazy<Task<IBrowser>>(() => browserType.LaunchAsync(launchOptions), LazyThreadSafetyMode.ExecutionAndPublication));
        return lazy.Value;
    }

    public static async Task CloseAllAsync()
    {
        foreach (var pair in Browsers)
        {
            if (!pair.Value.IsValueCreated) continue;
            try { var browser = await pair.Value.Value.ConfigureAwait(false); await browser.CloseAsync().ConfigureAwait(false); } catch { }
        }
        Browsers.Clear();
    }

    private static string CreateKey(string browserName, BrowserTypeLaunchOptions options)
    {
        var headless = options.Headless?.ToString() ?? "default";
        var channel = options.Channel ?? "default";
        return $"{browserName}|headless={headless}|channel={channel}";
    }
}
""")

    write_text(COMPAT_PROJECT_ROOT / "CVISBrowserTest.cs", """using Microsoft.Playwright;
using NUnit.Framework;
using NUnit.Framework.Interfaces;

namespace CVIS.Playwright.NUnitCompat;

public abstract class CVISBrowserTest : CVISPlaywrightTest
{
    private readonly List<IBrowserContext> _contexts = new();
    public IBrowser Browser { get; private set; } = null!;

    [SetUp]
    public async Task CVISBrowserSetupAsync()
    {
        var connectOptions = await ConnectOptionsAsync().ConfigureAwait(false);
        if (connectOptions is not null)
        {
            Browser = await BrowserType.ConnectAsync(connectOptions.Value.wsEndpoint, connectOptions.Value.options).ConfigureAwait(false);
            return;
        }
        Browser = await CVISBrowserService.GetOrLaunchAsync(BrowserType, await LaunchOptionsAsync().ConfigureAwait(false)).ConfigureAwait(false);
    }

    [TearDown]
    public async Task CVISBrowserTearDownAsync()
    {
        if (TestContext.CurrentContext.Result.Outcome.Status == TestStatus.Passed)
        {
            foreach (var context in _contexts) await context.CloseAsync().ConfigureAwait(false);
        }
        _contexts.Clear();
    }

    public async Task<IBrowserContext> NewContext(BrowserNewContextOptions? options = null)
    {
        var context = await Browser.NewContextAsync(options).ConfigureAwait(false);
        _contexts.Add(context);
        return context;
    }

    public virtual Task<BrowserTypeLaunchOptions> LaunchOptionsAsync() => Task.FromResult(CVISPlaywrightSettingsProvider.LaunchOptions);
    public virtual Task<(string wsEndpoint, BrowserTypeConnectOptions? options)?> ConnectOptionsAsync() => Task.FromResult<(string wsEndpoint, BrowserTypeConnectOptions? options)?>(null);
}
""")

    write_text(COMPAT_PROJECT_ROOT / "CVISContextTest.cs", """using Microsoft.Playwright;
using NUnit.Framework;

namespace CVIS.Playwright.NUnitCompat;

public abstract class CVISContextTest : CVISBrowserTest
{
    public IBrowserContext Context { get; private set; } = null!;

    [SetUp]
    public async Task CVISContextSetupAsync()
    {
        Context = await NewContext(ContextOptions()).ConfigureAwait(false);
    }

    public virtual BrowserNewContextOptions ContextOptions() => new() { Locale = "en-US", ColorScheme = ColorScheme.Light };
}
""")

    write_text(COMPAT_PROJECT_ROOT / "CVISPageTest.cs", """using Microsoft.Playwright;
using NUnit.Framework;

namespace CVIS.Playwright.NUnitCompat;

public abstract class CVISPageTest : CVISContextTest
{
    public IPage Page { get; private set; } = null!;

    [SetUp]
    public async Task CVISPageSetupAsync()
    {
        Page = await Context.NewPageAsync().ConfigureAwait(false);
    }
}
""")

    write_text(COMPAT_PROJECT_ROOT / "CVISApiTest.cs", """using Microsoft.Playwright;
using NUnit.Framework;

namespace CVIS.Playwright.NUnitCompat;

public abstract class CVISApiTest : CVISPlaywrightTest
{
    public IAPIRequestContext ApiContext { get; private set; } = null!;

    [SetUp]
    public async Task CVISApiSetupAsync()
    {
        ApiContext = await Playwright.APIRequest.NewContextAsync(ApiRequestOptions()).ConfigureAwait(false);
    }

    [TearDown]
    public async Task CVISApiTearDownAsync()
    {
        if (ApiContext is not null) await ApiContext.DisposeAsync().ConfigureAwait(false);
    }

    public virtual APIRequestNewContextOptions ApiRequestOptions() => new() { IgnoreHTTPSErrors = true };
    public async Task<IAPIRequestContext> NewApiRequestContextAsync(APIRequestNewContextOptions? options = null) => await Playwright.APIRequest.NewContextAsync(options ?? ApiRequestOptions()).ConfigureAwait(false);
}
""")

    write_text(COMPAT_PROJECT_ROOT / "CVISPlaywrightFeatureCatalog.md", """# CVIS Playwright NUnit Compatibility Layer Feature Catalog

This project recreates the practical features of `Microsoft.Playwright.NUnit` under CVIS-owned base classes.

| Microsoft.Playwright.NUnit | CVIS replacement |
|---|---|
| `PlaywrightTest` | `CVISPlaywrightTest` |
| `BrowserTest` | `CVISBrowserTest` |
| `ContextTest` | `CVISContextTest` |
| `PageTest` | `CVISPageTest` |
| API support | `CVISApiTest` |
| Settings provider | `CVISPlaywrightSettingsProvider` |
| Browser service | `CVISBrowserService` |

Recreated behavior includes NUnit setup lifecycle, shared Playwright runtime, browser selection from environment, browser type resolution, data-testid selector configuration, Expect helpers, default expect timeout support, browser launch, browser context tracking, context cleanup, default context options, page creation, and API request context creation.
""")

def add_project_reference_to_tests() -> None:
    tree = ET.parse(TEST_CSPROJ)
    root = tree.getroot()
    relative_project_path = r"..\CVIS.Playwright.NUnitCompat\CVIS.Playwright.NUnitCompat.csproj"
    for project_ref in root.findall(".//ProjectReference"):
        if project_ref.attrib.get("Include", "").lower() == relative_project_path.lower():
            return
    item_group = ET.SubElement(root, "ItemGroup")
    project_ref = ET.SubElement(item_group, "ProjectReference")
    project_ref.set("Include", relative_project_path)
    indent_xml(root)
    tree.write(TEST_CSPROJ, encoding="utf-8", xml_declaration=True)

def write_tests() -> None:
    write_text(TEST_COMPAT_ROOT / "CVISPlaywrightSettingsProviderTests.cs", """using CVIS.Playwright.NUnitCompat;
using Microsoft.Playwright;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Shared.PlaywrightCompatTests;

[TestFixture]
[Category("CVISPlaywrightCompat")]
public sealed class CVISPlaywrightSettingsProviderTests
{
    [Test]
    public void BrowserName_ShouldDefaultToChromium()
    {
        using var scope = new EnvironmentScope("BROWSER", null);
        using var cvisScope = new EnvironmentScope("CVIS_PLAYWRIGHT_BROWSER", null);
        Assert.That(CVISPlaywrightSettingsProvider.BrowserName, Is.EqualTo(BrowserType.Chromium));
    }

    [Test]
    public void BrowserName_ShouldReadCvisBrowserEnvironmentVariable()
    {
        using var scope = new EnvironmentScope("BROWSER", null);
        using var cvisScope = new EnvironmentScope("CVIS_PLAYWRIGHT_BROWSER", BrowserType.Firefox);
        Assert.That(CVISPlaywrightSettingsProvider.BrowserName, Is.EqualTo(BrowserType.Firefox));
    }

    [Test]
    public void BrowserName_ShouldRejectInvalidBrowser()
    {
        using var scope = new EnvironmentScope("BROWSER", "not-a-browser");
        Assert.Throws<ArgumentException>(() => _ = CVISPlaywrightSettingsProvider.BrowserName);
    }

    [Test]
    public void LaunchOptions_ShouldHonorHeadedEnvironmentVariable()
    {
        using var scope = new EnvironmentScope("HEADED", "1");
        Assert.That(CVISPlaywrightSettingsProvider.LaunchOptions.Headless, Is.False);
    }

    private sealed class EnvironmentScope : IDisposable
    {
        private readonly string _name;
        private readonly string? _originalValue;
        public EnvironmentScope(string name, string? value) { _name = name; _originalValue = Environment.GetEnvironmentVariable(name); Environment.SetEnvironmentVariable(name, value); }
        public void Dispose() => Environment.SetEnvironmentVariable(_name, _originalValue);
    }
}
""")

    write_text(TEST_COMPAT_ROOT / "LoopbackHttpServer.cs", """using System.Net;
using System.Net.Sockets;
using System.Text;

namespace CVIS.Automation.Tests.Shared.PlaywrightCompatTests;

internal sealed class LoopbackHttpServer : IAsyncDisposable
{
    private readonly TcpListener _listener;
    private readonly CancellationTokenSource _cancellation = new();
    private readonly Task _acceptLoop;
    public Uri Uri { get; }

    public LoopbackHttpServer()
    {
        _listener = new TcpListener(IPAddress.Loopback, 0);
        _listener.Start();
        var port = ((IPEndPoint)_listener.LocalEndpoint).Port;
        Uri = new Uri($"http://127.0.0.1:{port}/probe");
        _acceptLoop = Task.Run(AcceptLoopAsync);
    }

    private async Task AcceptLoopAsync()
    {
        while (!_cancellation.IsCancellationRequested)
        {
            try
            {
                using var client = await _listener.AcceptTcpClientAsync(_cancellation.Token);
                await using var stream = client.GetStream();
                var buffer = new byte[2048];
                _ = await stream.ReadAsync(buffer, _cancellation.Token);
                var body = "CVIS Playwright compatibility probe OK";
                var bodyBytes = Encoding.UTF8.GetBytes(body);
                var header = "HTTP/1.1 200 OK\r\n" + "Content-Type: text/plain; charset=utf-8\r\n" + $"Content-Length: {bodyBytes.Length}\r\n" + "Connection: close\r\n" + "\r\n";
                var headerBytes = Encoding.ASCII.GetBytes(header);
                await stream.WriteAsync(headerBytes, _cancellation.Token);
                await stream.WriteAsync(bodyBytes, _cancellation.Token);
            }
            catch (OperationCanceledException) { break; }
            catch { }
        }
    }

    public async ValueTask DisposeAsync()
    {
        _cancellation.Cancel();
        _listener.Stop();
        try { await _acceptLoop; } catch { }
        _cancellation.Dispose();
    }
}
""")

    write_text(TEST_COMPAT_ROOT / "CVISPlaywrightTestCompatTests.cs", """using CVIS.Playwright.NUnitCompat;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Shared.PlaywrightCompatTests;

[TestFixture]
[Category("CVISPlaywrightCompat")]
public sealed class CVISPlaywrightTestCompatTests : CVISPlaywrightTest
{
    [Test]
    public void PlaywrightTest_ShouldInitializeRuntimeAndBrowserType()
    {
        Assert.That(Playwright, Is.Not.Null);
        Assert.That(BrowserName, Is.Not.Empty);
        Assert.That(BrowserType, Is.Not.Null);
    }
}
""")

    write_text(TEST_COMPAT_ROOT / "CVISApiTestCompatTests.cs", """using CVIS.Playwright.NUnitCompat;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Shared.PlaywrightCompatTests;

[TestFixture]
[Category("CVISPlaywrightCompat")]
public sealed class CVISApiTestCompatTests : CVISApiTest
{
    [Test]
    public async Task ApiTest_ShouldCreateApiContextAndPerformRealPlaywrightRequest()
    {
        Assert.That(ApiContext, Is.Not.Null);
        await using var server = new LoopbackHttpServer();
        var response = await ApiContext.GetAsync(server.Uri.ToString());
        Assert.That(response.Ok, Is.True);
        var body = await response.TextAsync();
        Assert.That(body, Does.Contain("CVIS Playwright compatibility probe OK"));
    }

    [Test]
    public async Task ApiTest_ShouldCreateAdditionalApiRequestContext()
    {
        await using var context = await NewApiRequestContextAsync();
        Assert.That(context, Is.Not.Null);
    }
}
""")

    write_text(TEST_COMPAT_ROOT / "CVISContextDefaultsCompatTests.cs", """using CVIS.Playwright.NUnitCompat;
using Microsoft.Playwright;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Shared.PlaywrightCompatTests;

[TestFixture]
[Category("CVISPlaywrightCompat")]
public sealed class CVISContextDefaultsCompatTests
{
    [Test]
    public void ContextOptions_ShouldDefaultToExpectedValues()
    {
        var host = new ContextHost();
        var options = host.ContextOptions();
        Assert.That(options.Locale, Is.EqualTo("en-US"));
        Assert.That(options.ColorScheme, Is.EqualTo(ColorScheme.Light));
    }
    private sealed class ContextHost : CVISContextTest { }
}
""")

    write_text(TEST_COMPAT_ROOT / "CVISPageTestBrowserCompatTests.cs", """using CVIS.Playwright.NUnitCompat;
using NUnit.Framework;

namespace CVIS.Automation.Tests.Shared.PlaywrightCompatTests;

[TestFixture]
[Category("CVISPlaywrightCompat")]
public sealed class CVISPageTestBrowserCompatTests : CVISPageTest
{
    [Test]
    [Explicit("Requires Playwright browsers installed. Run manually when validating browser-backed CVISPageTest.")]
    public async Task PageTest_ShouldCreateBrowserContextAndPage()
    {
        Assert.That(Browser, Is.Not.Null);
        Assert.That(Context, Is.Not.Null);
        Assert.That(Page, Is.Not.Null);
        await Page.SetContentAsync("<html><head><title>CVIS</title></head><body><h1 data-testid='title'>OK</h1></body></html>");
        await Expect(Page).ToHaveTitleAsync("CVIS");
    }
}
""")

def add_projects_to_solution_if_present() -> None:
    solution_files = list(SOLUTION_ROOT.glob("*.sln"))
    if not solution_files: return
    solution_path = solution_files[0]
    for project in [COMPAT_CSPROJ, TEST_CSPROJ]:
        try:
            subprocess.run(["dotnet", "sln", str(solution_path), "add", str(project)], cwd=SOLUTION_ROOT, check=False, capture_output=True, text=True)
        except Exception:
            pass

def main() -> None:
    require_layout()
    create_compat_project()
    write_compat_files()
    add_project_reference_to_tests()
    write_tests()
    add_projects_to_solution_if_present()
    print("Added CVIS.Playwright.NUnitCompat class library and compatibility tests.")
    print("No PolicyDrift tests were replaced by this package.")

if __name__ == "__main__":
    main()
