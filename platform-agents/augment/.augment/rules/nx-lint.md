---
type: agent_requested
description: "Linting in Nx monorepos: running lints per project, on affected sets, and with parallel execution."
---

# nx-lint

Linting in Nx monorepos: running lints per project, on affected sets, and with parallel execution.

## Instructions

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