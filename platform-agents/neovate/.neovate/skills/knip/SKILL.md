---
name: "knip"
description: "Finds unused files, exports, and dependencies with knip, the JavaScript dead-code detective, including plugin configs. Use when working with knip scan, knip config, code quality or when the user mentions knip scan, knip config, code quality."
license: "MIT"
compatibility: "Requires npx."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "code-quality"}
allowed-tools: "Glob Grep Read Bash(npx:*)"
---

Finds unused files, exports, and dependencies with knip, the JavaScript dead-code detective, including plugin configs.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx knip`, `npx knip --init`
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

# Knip

Find dead code in JavaScript projects.

## When to Use

- Removing unused files, exports, and dependencies
- Cleaning monorepos where packages hide usage
- Reducing bundle size and install time
- Pre-merge CI checks for dead code regressions

## Commands

```bash
# Scan
npx knip

# Production-only concerns
npx knip --production

# Scope
npx knip --include files,dependencies
npx knip --include exports

# Reports
npx knip --json > knip-report.json
npx knip --reporter codeowners

# Init and debug
npx knip --init
npx knip --debug

# Auto-fix dependencies
npx knip --fix --include dependencies
```

## Config Example

```json
{
  "entry": ["src/index.ts", "scripts/*.ts"],
  "ignore": ["src/generated/**"],
  "ignoreDependencies": ["@types/node"]
}
```

## Best Practices

- Run knip in CI on every merge
- Define entry points explicitly for CLI tools
- Ignore generated directories and bundled output
- Review the report before bulk-deleting files
- Use --include exports to find dead public API surface
- Treat new dead code as a build failure

## Capabilities

### knip-scan
Scan projects for dead code.

**Parameters:**
- `include` (string): files, exports, dependencies
- `reporter` (string): default, json, codeowners

**Commands:**
- `npx knip`
- `npx knip --production`
- `npx knip --no-gitignore`
- `npx knip --include files,dependencies`
- `npx knip --reporter json`

**Examples:**
- npx knip --json > knip-report.json
- npx knip --include exports --tags owner
- npx knip --config knip.jsonc

### knip-config
Configure entry points and ignore rules.

**Parameters:**
- `fix` (boolean): Fix issues where possible
- `workspace` (string): Workspace glob

**Commands:**
- `npx knip --init`
- `npx knip --debug`
- `npx knip --fix`
- `npx knip --dependencies`

**Examples:**
- npx knip --fix --include dependencies
- npx knip --workspace packages/*

## References
- [Knip Docs](https://knip.dev)
- [Knip on GitHub](https://github.com/webpro/knip)
