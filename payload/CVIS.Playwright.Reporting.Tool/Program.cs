using CVIS.Playwright.Reporting;
using CVIS.Playwright.Reporting.Models;

var arguments = Arguments.Parse(args);

var options = new CvisReportBuildOptions
{
    FrameworkName = arguments.Get("--framework-name", "CVIS Authoritative Test Run"),
    TrxRoot = arguments.Require("--trx-root"),
    NUnitXmlRoot = arguments.Require("--nunit-xml-root"),
    OutputRoot = arguments.Require("--output-root"),
    MinimumTotal = int.Parse(arguments.Get("--minimum-total", "1"))
};

var summary = new NUnitResultReportBuilder().Build(options);

Console.WriteLine($"Created authoritative report: {Path.Combine(options.OutputRoot, "cpn-report.html")}");
Console.WriteLine($"Total: {summary.Total}; Passed: {summary.Passed}; Failed: {summary.Failed}; Skipped: {summary.Skipped}; Other: {summary.Other}");

internal sealed class Arguments
{
    private readonly Dictionary<string, string> _values;

    private Arguments(Dictionary<string, string> values)
    {
        _values = values;
    }

    public static Arguments Parse(string[] args)
    {
        var values = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);

        for (var index = 0; index < args.Length; index++)
        {
            var key = args[index];

            if (!key.StartsWith("--", StringComparison.Ordinal))
            {
                continue;
            }

            if (index + 1 >= args.Length)
            {
                throw new ArgumentException($"Missing value for argument {key}");
            }

            values[key] = args[index + 1];
            index++;
        }

        return new Arguments(values);
    }

    public string Require(string key)
    {
        if (!_values.TryGetValue(key, out var value) || string.IsNullOrWhiteSpace(value))
        {
            throw new ArgumentException($"Missing required argument {key}");
        }

        return value;
    }

    public string Get(string key, string fallback)
    {
        return _values.TryGetValue(key, out var value) && !string.IsNullOrWhiteSpace(value)
            ? value
            : fallback;
    }
}
