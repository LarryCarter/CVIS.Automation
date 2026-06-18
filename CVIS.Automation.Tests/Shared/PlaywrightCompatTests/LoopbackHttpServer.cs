using System.Net;
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
                var header = "HTTP/1.1 200 OK
" + "Content-Type: text/plain; charset=utf-8
" + $"Content-Length: {bodyBytes.Length}
" + "Connection: close
" + "
";
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
