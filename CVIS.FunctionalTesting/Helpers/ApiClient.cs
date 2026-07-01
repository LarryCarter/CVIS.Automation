using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using CVIS.FunctionalTesting.Config;

namespace CVIS.FunctionalTesting.Helpers;

/// <summary>
/// Lightweight HTTP helper for API functional tests.
/// No Playwright dependency.
/// </summary>
public sealed class ApiClient : IDisposable
{
    private readonly HttpClient _client;
    private readonly JsonSerializerOptions _jsonOptions = new()
    {
        PropertyNameCaseInsensitive = true
    };

    private bool _disposed;

    public ApiClient(FunctionalTestConfig config, string? baseUrl = null)
    {
        _client = new HttpClient
        {
            BaseAddress = new Uri(baseUrl ?? config.ApiBaseUrl),
            Timeout = TimeSpan.FromMilliseconds(config.DefaultTimeoutMilliseconds)
        };

        if (!string.IsNullOrWhiteSpace(config.Api.AuthToken))
        {
            _client.DefaultRequestHeaders.Authorization =
                new AuthenticationHeaderValue("Bearer", config.Api.AuthToken);
        }
    }

    public async Task<T?> GetJsonAsync<T>(string path, CancellationToken cancellationToken = default)
    {
        using var response = await _client.GetAsync(path, cancellationToken).ConfigureAwait(false);
        response.EnsureSuccessStatusCode();

        await using var stream = await response.Content.ReadAsStreamAsync(cancellationToken).ConfigureAwait(false);
        return await JsonSerializer.DeserializeAsync<T>(stream, _jsonOptions, cancellationToken).ConfigureAwait(false);
    }

    public async Task<HttpResponseMessage> GetAsync(string path, CancellationToken cancellationToken = default)
    {
        return await _client.GetAsync(path, cancellationToken).ConfigureAwait(false);
    }

    public async Task<HttpResponseMessage> PostJsonAsync<T>(
        string path,
        T body,
        CancellationToken cancellationToken = default)
    {
        var json = JsonSerializer.Serialize(body, _jsonOptions);
        using var content = new StringContent(json, Encoding.UTF8, "application/json");

        return await _client.PostAsync(path, content, cancellationToken).ConfigureAwait(false);
    }

    public void Dispose()
    {
        if (_disposed)
        {
            return;
        }

        _client.Dispose();
        _disposed = true;
    }
}
