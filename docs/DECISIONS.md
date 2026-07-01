# Architecture Decisions

## 2026-07-01 — Capability Base Classes

Decision: Use capability-based base classes instead of domain-specific base classes.

Accepted base classes:

```text
BaseAutomationCvisTest
BaseAutomationCvisApiTest
BaseAutomationCvisDatabaseTest
BaseAutomationCvisPlaywrightBrowserTest
BaseAutomationCvisPlaywrightPageTabTest
```

Rejected pattern:

```text
PolicyDriftBaseTest
UnityBaseTest
LegacySustainmentBaseTest
```

Reason: domains may use API, database, browser, or normal automation capabilities. Capability-based inheritance keeps the hierarchy shallow and predictable.

## 2026-07-01 — Authoritative Reporting Source

Decision: authoritative reporting comes from TRX/NUnit XML, not lifecycle teardown logs.

Reason: HyperExecute and Visual Studio both rely on runner outputs. Lifecycle logs only describe tests that pass through framework hooks.
