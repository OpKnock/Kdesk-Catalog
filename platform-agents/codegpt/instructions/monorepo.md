# monorepo

Manages monorepo builds with pnpm workspaces, Turborepo, and Nx: task orchestration, affected builds, versioning, and changesets.

## Instructions

# Monorepo Engineering

Structure and run multi-package repositories efficiently.

## What This Skill Does

- Manages pnpm workspaces and package filters
- Orchestrates tasks with Turborepo/Nx caching
- Runs affected-only tasks on CI
- Versions packages with changesets
- Handles cross-package dependency graphs

## When to Use

- Multi-package JS/TS repos sharing tooling
- CI builds taking too long (caching/affected)
- Publishing multiple packages in lockstep

## Real Commands

```bash
# pnpm workspaces
pnpm -r test
pnpm --filter @org/api test
pnpm -r --workspace-concurrency=4 build
pnpm -F @org/web add lodash
pnpm list -r --depth=-1

# Turborepo
npx turbo run build
npx turbo run lint --filter=@org/api
npx turbo run test --affected --base=origin/main
npx turbo run dev --parallel

# Nx
nx affected -t build --base=main
nx run-many -t test --projects=@org/api,@org/web
nx graph

# Versioning
npx changeset add
npx changeset version
npx changeset publish
```

## Best Practices

- Use filter/affected to keep CI fast and focused
- Commit turbo/nx cache config; enable remote caching
- One lockfile, consistent dependency versions across packages
- Use changesets for atomic version decisions
- Keep build-time dependencies shallow; use workspace:* protocols

## Capabilities

### workspace-commands
Run commands across workspace packages with pnpm.

**Commands:**
- `pnpm -r test`
- `pnpm --filter @org/api test`
- `pnpm -r --workspace-concurrency=4 build`
- `pnpm -F @org/web add lodash`
- `pnpm list -r --depth=-1`

**Examples:**
- pnpm -r test
- pnpm --filter @org/api test
- pnpm -F @org/web add lodash

### task-orchestration
Orchestrate build tasks and version packages with Turborepo/Nx and changesets.

**Commands:**
- `npx turbo run build`
- `npx turbo run lint --filter=@org/api`
- `npx turbo run test --affected --base=origin/main`
- `nx affected -t build --base=main`
- `npx changeset add`
- `npx changeset version`

**Examples:**
- npx turbo run build
- npx turbo run test --affected --base=origin/main
- npx changeset version
