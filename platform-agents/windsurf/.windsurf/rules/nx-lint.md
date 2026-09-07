---
trigger: glob
description: "Linting in Nx monorepos: running lints per project, on affected sets, and with parallel execution. Use when working with nx lint, code quality or when the user mentions nx lint, code quality."
globs: ["**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

Linting in Nx monorepos: running lints per project, on affected sets, and with parallel execution.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx nx lint web`
- Check `knowledge` references and prerequisites before proceeding

### 2. Reason
Analyze and plan:
- Compare current state vs desired state (drift, checksums, policy)
- Evaluate trust, compatibility, and risk: use `kdesk trust` and `kdesk doctor` patterns
- Decide: which capabilities/tools are needed, which can be skipped

### 3. Act
Execute with guards:
- Run only `allowed-tools` (see frontmatter); use `safe_path` for writes
- Prefer `Bash` with explicit binaries (`curl`, `kubectl`, `kdesk`) over generic shell
- Record evidence: file paths, checksums, and tool outputs for verification

# Nx Lint

Run ESLint (or other linters) across Nx monorepo projects with caching and
affected-graph awareness.

## When to Use

- Linting all projects in a monorepo
- Linting only projects affected by a PR
- Fixing lint errors with caching for fast iteration

## Real Commands

```bash
# Lint one project
npx nx lint web

# Lint every project that has a lint target
npx nx run-many -t lint

# Lint only projects touched by the current branch
npx nx affected -t lint

# With explicit base for CI
npx nx affected -t lint --base=origin/main

# Auto-fix + parallel
npx nx run-many -t lint --fix --parallel=5

# Bypass cache when you changed config files
npx nx lint web --skip-nx-cache
```

## CI Example

```yaml
- name: Lint affected
  run: npx nx affected -t lint --base=origin/main --parallel=3
```

## Best Practices

- Always use `--base` explicitly in CI; don't rely on the git merge-base default
- Invalidate cache deliberately with `--skip-nx-cache` after changing eslint config
- Lint+test+build in one run: `npx nx affected -t lint test build`
- Keep `lint` target present in every project.json for `run-many` to pick it up

## Example Response

Returns per-project lint results with the number of errors, and shows which projects
were skipped because they were unaffected and cached.

## Capabilities

### nx-lint
Run lint targets across Nx projects and affected graph

**Parameters:**
- `affected` (boolean): Run lint only on projects affected by the changed files
- `base` (string): Base commit for the affected graph, e.g. main~1
- `parallel` (integer): Maximum number of projects linted in parallel

**Commands:**
- `npx nx lint web`
- `npx nx run-many -t lint`
- `npx nx affected -t lint`
- `npx nx lint web --fix`
- `npx nx run-many -t lint --parallel=5 --maxParallel=5`

**Examples:**
- npx nx affected -t lint --base=main~1
- npx nx run-many -t lint --projects=web,api
- npx nx lint api --skip-nx-cache

## References
- [Nx linting guide](https://nx.dev/features/lint-project)
- [nx run-many reference](https://nx.dev/nx-api/nx/documents/run-many)
