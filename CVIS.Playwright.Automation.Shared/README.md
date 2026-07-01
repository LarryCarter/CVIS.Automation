# CVIS.Playwright.Automation.Shared

Shared helpers used by automation projects.

## Purpose

Use this project for reusable utilities that are not test base classes.

Examples:

- shared assertions
- test data helpers
- file helpers
- report helpers
- reusable service clients

## Rules

Do not put Playwright browser lifecycle here. That belongs in `CVIS.Playwright.NUnitCompat`.

Do not put authoritative report generation here. That belongs in `CVIS.Playwright.Reporting`.
