---
trigger: glob
description: "Manages monorepo builds with pnpm workspaces, Turborepo, and Nx: task orchestration, affected builds, versioning, and changesets. Use when working with workspace commands, task orchestration, devtools or when the user mentions workspace commands, task orchestration, devtools."
globs: ["**/*.r", "**/*.sh"]
---

Manages monorepo builds with pnpm workspaces, Turborepo, and Nx: task orchestration, affected builds, versioning, and changesets.

## Agentic Workflow: Read -> Reason -> Act (monorepo)

You are **monorepo** (devtools/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devtools context for `monorepo`
- Domain: Manages monorepo builds with pnpm workspaces, Turborepo, and Nx: task orchestration, affected builds, versioning, and changesets.
- **workspace-commands**: Run commands across workspace packages with pnpm. — `pnpm -r test`
- **task-orchestration**: Orchestrate build tasks and version packages with Turborepo/Nx and changesets. — `npx turbo run build`
- Check `knowledge` and `prerequisites: npx, pnpm`

### 2. Reason — think for `monorepo`
- For `workspace-commands`: Run commands across workspace packages with pnpm. — decide which checks to run
- For `task-orchestration`: Orchestrate build tasks and version packages with Turborepo/Nx and changesets. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `monorepo` tools
- Tools: `Glob`, `Grep`, `Read`, `Pnpm`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `monorepo:337f9354`

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

**Parameters:**
- `filter` (string): Package filter, e.g. @org/api
- `recursive` (boolean): Run in all workspaces (-r)

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

**Parameters:**
- `task` (string): Task name, e.g. build, test, lint
- `affected` (boolean): Run only for changed packages

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

## References
- [Turborepo Documentation](https://turborepo.dev/docs)
- [Nx Documentation](https://nx.dev/)
- [pnpm Workspaces](https://pnpm.io/workspaces)
- [Changesets](https://github.com/changesets/changesets)
