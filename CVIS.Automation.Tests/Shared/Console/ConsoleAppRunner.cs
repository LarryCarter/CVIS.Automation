using System.Diagnostics;

namespace CVIS.Automation.Tests.Shared.Console;

public sealed class ConsoleAppRunner
{
    public async Task<ConsoleRunResult> RunAsync(
        string executablePath,
        string arguments,
        string workingDirectory,
        IDictionary<string, string?>? environmentVariables = null,
        int timeoutSeconds = 120)
    {
        if (!File.Exists(executablePath))
        {
            throw new FileNotFoundException($"Console executable was not found: {executablePath}");
        }

        if (!Directory.Exists(workingDirectory))
        {
            throw new DirectoryNotFoundException($"Working directory was not found: {workingDirectory}");
        }

        var startInfo = new ProcessStartInfo
        {
            FileName = executablePath,
            Arguments = arguments,
            WorkingDirectory = workingDirectory,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false,
            CreateNoWindow = true
        };

        if (environmentVariables is not null)
        {
            foreach (var pair in environmentVariables)
            {
                startInfo.Environment[pair.Key] = pair.Value;
            }
        }

        using var process = new Process
        {
            StartInfo = startInfo
        };

        process.Start();

        var stdoutTask = process.StandardOutput.ReadToEndAsync();
        var stderrTask = process.StandardError.ReadToEndAsync();

        var completed = await Task.Run(() => process.WaitForExit(timeoutSeconds * 1000));

        if (!completed)
        {
            try
            {
                process.Kill(entireProcessTree: true);
            }
            catch
            {
                // Best-effort cleanup.
            }

            throw new TimeoutException(
                $"Console app timed out after {timeoutSeconds} seconds: {executablePath} {arguments}");
        }

        return new ConsoleRunResult
        {
            ExitCode = process.ExitCode,
            StandardOutput = await stdoutTask,
            StandardError = await stderrTask
        };
    }
}
