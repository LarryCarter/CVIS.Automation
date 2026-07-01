using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using CVIS.FunctionalTesting.Config;

namespace CVIS.FunctionalTesting.Helpers;

/// <summary>
/// HTTP helper for API functional tests. No Playwright dependency.
/// Use in tests that inherit BaseAutomationCvisApiTest.
/// </summary>
public sealed class ApiClient : IDisposable
{
    private readonly HttpClient _client;
    private readonly JsonSerializerOptions _jsonOptions;
    private bool _disposed;

    public ApiClient(FunctionalTestConfig config, string? baseUrl = null)
    {
        _client = new HttpClient
        {
            BaseAddress = new Uri(baseUrl ?? config.ApiBaseUrl),
            Timeout = TimeSpan.FromMilliseconds(config.DefaultTimeoutMs)
        };

        _jsonOptions = new JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = true
        };

        if (!string.IsNullOrWhiteSpace(config.Api.AuthToken))
        {
            _client.DefaultRequestHeaders.Authorization =
                new AuthenticationHeaderValue("Bearer", config.Api.AuthToken);
        }
    }

    public Task<HttpResponseMessage> GetAsync(string path) =>
        _client.GetAsync(path);

    public async Task<T?> GetJsonAsync<T>(string path)
    {
        var response = await _client.GetAsync(path);
        response.EnsureSuccessStatusCode();
        var json = await response.Content.ReadAsStringAsync();
        return JsonSerializer.Deserialize<T>(json, _jsonOptions);
    }

    public Task<HttpResponseMessage> PostJsonAsync<T>(string path, T payload) =>
        _client.PostAsync(path, Serialize(payload));

    public Task<HttpResponseMessage> PutJsonAsync<T>(string path, T payload) =>
        _client.PutAsync(path, Serialize(payload));

    public Task<HttpResponseMessage> DeleteAsync(string path) =>
        _client.DeleteAsync(path);

    public void Dispose()
    {
        if (!_disposed)
        {
            _client.Dispose();
            _disposed = true;
        }
    }

    private StringContent Serialize<T>(T payload) =>
        new(JsonSerializer.Serialize(payload, _jsonOptions), Encoding.UTF8, "application/json");
}
