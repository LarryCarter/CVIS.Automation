# CVIS Repository README Standard

# Purpose

This document defines the standard structure for README.md files in major CVIS.Automation folders.

# Responsibilities

Every major folder README must help developers and AI tools answer:

- What is this folder for?
- When should I use it?
- When should I not use it?
- What examples show the correct pattern?

# When to use

Use this standard whenever creating or updating documentation in a major repository folder.

# When NOT to use

Do not use this standard to replace formal architecture decision records. Use `docs/DECISIONS.md` through DocOps for cumulative decisions.

# Architecture

Every major folder README should use these sections:

```markdown
# Purpose

# Responsibilities

# When to use

# When NOT to use

# Architecture

# Examples

# Common mistakes

# Related folders
```

# Examples

Folder README files should include at least one code example or command example when the folder contains executable code, base classes, scripts, or tooling.

# Common mistakes

- Writing a README that only lists classes.
- Omitting when not to use the folder.
- Omitting examples for base class selection.
- Forgetting AI-facing guidance when the folder is likely to be used by Copilot or other coding assistants.

# Related folders

- `CVIS.FunctionalTesting`
- `CVIS.Playwright.NUnitCompat`
- `CVIS.Automation.Tests`
- `scripts`
