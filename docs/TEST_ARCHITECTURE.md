# CVIS Test Architecture

## Architecture principle

NUnit is the spine. Capabilities are added only when needed.

## Base class tree

```text
BaseAutomationCvisTest
├── BaseAutomationCvisApiTest
├── BaseAutomationCvisDatabaseTest
└── BaseAutomationCvisPlaywrightBrowserTest
    └── BaseAutomationCvisPlaywrightPageTabTest
```

## Domain projects

PolicyDrift, Unity, LegacySustainment, and future domains are not base classes.

A domain can have tests that use any capability base:

```text
PolicyDrift API test       -> BaseAutomationCvisApiTest
PolicyDrift DB test        -> BaseAutomationCvisDatabaseTest
PolicyDrift UI test        -> BaseAutomationCvisPlaywrightPageTabTest
Unity DB test              -> BaseAutomationCvisDatabaseTest
Legacy config test         -> BaseAutomationCvisTest
```

## Reporting

Test execution produces:

```text
TestResults\TRX
TestResults\NUnitXml
```

The report tool generates:

```text
TestResults\CPN\cpn-report.html
```

HyperExecute parses:

```text
TestResults\NUnitXml
```
