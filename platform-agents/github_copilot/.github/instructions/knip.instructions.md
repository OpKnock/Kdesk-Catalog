---
applyTo: "**/*.java **/*.json **/*.r **/*.sh **/*.{js,ts,jsx,tsx}"
---

Finds unused files, exports, and dependencies with knip, the JavaScript dead-code detective, including plugin configs.

## Agentic Workflow: Read -> Reason -> Act (knip)

You are **knip** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `knip`
- Domain: Finds unused files, exports, and dependencies with knip, the JavaScript dead-code detective, including plugin configs.
- **knip-scan**: Scan projects for dead code. — `npx knip`
- **knip-config**: Configure entry points and ignore rules. — `npx knip --init`
- Check `knowledge` and `prerequisites: npx`

### 2. Reason — think for `knip`
- For `knip-scan`: Scan projects for dead code. — decide which checks to run
- For `knip-config`: Configure entry points and ignore rules. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `knip` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `knip:1845fb4b`

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
