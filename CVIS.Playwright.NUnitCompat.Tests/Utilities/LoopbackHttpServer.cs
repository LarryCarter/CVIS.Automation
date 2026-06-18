using System.Net;
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
                headerBuilder.Append("HTTP/1.1 200 OK\r\n");
                headerBuilder.Append("Content-Type: text/plain; charset=utf-8\r\n");
                headerBuilder.Append("Content-Length: ");
                headerBuilder.Append(bodyBytes.Length);
                headerBuilder.Append("\r\n");
                headerBuilder.Append("Connection: close\r\n");
                headerBuilder.Append("\r\n");

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
