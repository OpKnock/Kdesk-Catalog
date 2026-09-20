---
name: "turbo-lint"
description: "Runs lint targets across Turborepo monorepos with caching, filters, and affected-scope execution. Use when working with turbo lint, code quality or when the user mentions turbo lint, code quality."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
alwaysApply: false
---

Runs lint targets across Turborepo monorepos with caching, filters, and affected-scope execution.

## Agentic Workflow: Read -> Reason -> Act (turbo-lint)

You are **turbo-lint** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `turbo-lint`
- Domain: Runs lint targets across Turborepo monorepos with caching, filters, and affected-scope execution.
- **turbo-lint**: Execute lint tasks in a Turborepo with caching and filtering — `npx turbo lint`
- Check `knowledge` and `prerequisites: npx`

### 2. Reason — think for `turbo-lint`
- For `turbo-lint`: Execute lint tasks in a Turborepo with caching and filtering — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `turbo-lint` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `turbo-lint:ea57cd1b`

# Turbo Lint

Runs lint tasks across a Turborepo with content-based caching so unchanged packages
are skipped entirely.

## When to Use

- Linting all packages in a monorepo
- Linting only affected packages per PR
- Combining lint+test+build in one cached pipeline

## Real Commands

```bash
# Lint every package with a lint script
npx turbo lint

# Lint one package
npx turbo run lint --filter=web

# Lint all packages in a scope
npx turbo run lint --filter=@acme/*

# Only packages affected since main
npx turbo run lint --affected --base=origin/main

# Don't stop on first failure
npx turbo lint --continue

# Run multiple tasks in one pipeline run
npx turbo run lint test build --affected --parallel
```

## Turbo Config (turbo.json)

```json
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "lint": {
      "dependsOn": ["^lint"],
      "outputs": []
    }
  }
}
```

## Best Practices

- Declare `lint` as a task so caching works consistently
- Use `--affected --base=origin/main` in CI to lint only PR changes
- Verify cache hits with `--output-logs=hash-only` or `--dry=json`
- Combine with `--continue` so one failing package doesn't mask others

## Example Response

Shows per-package task status (cached/full), durations, and error counts, with
`TURBO_CACHED` markers for skipped packages.

## Capabilities

### turbo-lint
Execute lint tasks in a Turborepo with caching and filtering

**Parameters:**
- `filter` (string): Include only matching packages, e.g. web or @acme/*
- `affected` (boolean): Run only packages affected by the change (uses git)
- `output-logs` (string): new-only, full, hash-only, none - log verbosity

**Commands:**
- `npx turbo lint`
- `npx turbo run lint --filter=web`
- `npx turbo run lint --affected`
- `npx turbo lint --continue`
- `npx turbo run lint --parallel --concurrency=6`

**Examples:**
- npx turbo run lint --filter=@acme/*
- npx turbo run lint test --affected --base=main
- npx turbo lint --output-logs=hash-only

## References
- [Turborepo docs](https://turbo.build/repo/docs)
- [Turbo filters](https://turbo.build/repo/docs/reference/filters)