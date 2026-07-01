
<!-- RDEL-DOCOPS-ID: F1839DE800530144 -->
<!-- RDEL-DOCOPS-SOURCE: .rdel-docops/memory/update.md -->
<!-- RDEL-DOCOPS-UTC: 2026-07-01 12:56:05Z -->

## Memory — CVIS Base Class Naming Standard

CVIS.Automation now prefers capability-based base classes over domain-specific base classes. New tests should not create `PolicyDriftBaseTest`, `UnityBaseTest`, or `LegacySustainmentBaseTest`.

Use:

- `BaseAutomationCvisTest` for normal no-browser NUnit tests.
- `BaseAutomationCvisApiTest` for API tests.
- `BaseAutomationCvisDatabaseTest` for SQL/database tests.
- `BaseAutomationCvisPlaywrightBrowserTest` for browser-level Playwright tests.
- `BaseAutomationCvisPlaywrightPageTabTest` for Playwright tests needing a fresh page/tab per test.

Every major folder should have a README.md following the repository README standard: Purpose, Responsibilities, When to use, When NOT to use, Architecture, Examples, Common mistakes, Related folders.

