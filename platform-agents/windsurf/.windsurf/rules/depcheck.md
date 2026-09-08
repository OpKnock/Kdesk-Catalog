---
trigger: glob
description: "Finds unused and missing dependencies with depcheck: unused imports, missing deps, and configuration analysis. Use when working with depcheck scan, depcheck cleanup, code quality or when the user mentions depcheck scan, depcheck cleanup, code quality."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

Finds unused and missing dependencies with depcheck: unused imports, missing deps, and configuration analysis.

## Agentic Workflow: Read -> Reason -> Act (depcheck)

You are **depcheck** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `depcheck`
- Domain: Finds unused and missing dependencies with depcheck: unused imports, missing deps, and configuration analysis.
- **depcheck-scan**: Scan projects for unused dependencies. — `npx depcheck`
- **depcheck-cleanup**: Remove unused dependencies safely. — `npm uninstall unused-package`
- Check `knowledge` and `prerequisites: npm, npx`

### 2. Reason — think for `depcheck`
- For `depcheck-scan`: Scan projects for unused dependencies. — decide which checks to run
- For `depcheck-cleanup`: Remove unused dependencies safely. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `depcheck` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `depcheck:e07ece1d`

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

**Parameters:**
- `ignores` (string): Packages to ignore
- `json` (boolean): JSON output
- `specials` (string): Special parsers: eslint, webpack

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

**Parameters:**
- `package` (string): Package name
- `save` (boolean): Update package.json on removal

**Commands:**
- `npm uninstall unused-package`
- `npm prune`
- `npm ls --depth=0`
- `npm ls unused-package`

**Examples:**
- npm ls --depth=0 | grep -v "deduped"
- npm uninstall lodash --save

## References
- [depcheck on GitHub](https://github.com/depcheck/depcheck)
- [npm Docs](https://docs.npmjs.com/cli/v10/commands/npm-uninstall)
