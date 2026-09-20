---
name: "knip"
description: "Finds unused files, exports, and dependencies with knip, the JavaScript dead-code detective, including plugin configs."
---

# knip

Finds unused files, exports, and dependencies with knip, the JavaScript dead-code detective, including plugin configs.

## Instructions

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

**Commands:**
- `npx knip --init`
- `npx knip --debug`
- `npx knip --fix`
- `npx knip --dependencies`

**Examples:**
- npx knip --fix --include dependencies
- npx knip --workspace packages/*
