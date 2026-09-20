---
type: agent_requested
description: "Finds unused and missing dependencies with depcheck: unused imports, missing deps, and configuration analysis."
---

# depcheck

Finds unused and missing dependencies with depcheck: unused imports, missing deps, and configuration analysis.

## Instructions

# depcheck

Find unused and missing dependencies.

## When to Use

- Cleaning up package.json bloat
- Catching dependencies used only via side-effect imports
- Verifying that every import resolves to an installed package
- Reducing install time and attack surface

## Commands

```bash
# Basic scan
npx depcheck

# JSON output for scripting
npx depcheck --json

# Ignore dev-tooling packages
npx depcheck --ignores="eslint,prettier,@types/*"

# Report missing dependencies too
npx depcheck --skip-missing=false

# Enable special parsers
npx depcheck --specials=eslint,webpack

# Verify remaining tree
npm ls --depth=0

# Remove what is unused
npm uninstall lodash
npm prune
```

## Best Practices

- Run depcheck before PRs that touch package.json
- Add @types/* and build tools to --ignores deliberately
- Review JSON output programmatically in CI
- Re-run tests after removing packages
- Update the lockfile with npm prune afterward
- Treat missing dependencies as a CI failure

## Capabilities

### depcheck-scan
Scan projects for unused dependencies.

**Commands:**
- `npx depcheck`
- `npx depcheck --json`
- `npx depcheck --ignores="eslint,prettier"`
- `npx depcheck --skip-missing=false`
- `npx depcheck --specials=eslint`

**Examples:**
- npx depcheck --json | python -m json.tool
- npx depcheck --ignores="@types/*,vitest"
- npx depcheck --config .depcheckrc

### depcheck-cleanup
Remove unused dependencies safely.

**Commands:**
- `npm uninstall unused-package`
- `npm prune`
- `npm ls --depth=0`
- `npm ls unused-package`

**Examples:**
- npm ls --depth=0 | grep -v "deduped"
- npm uninstall lodash --save