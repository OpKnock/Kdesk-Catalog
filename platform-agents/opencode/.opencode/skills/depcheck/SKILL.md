---
name: "depcheck"
description: "Finds unused and missing dependencies with depcheck: unused imports, missing deps, and configuration analysis. Use when working with depcheck scan, depcheck cleanup, code quality or when the user mentions depcheck scan, depcheck cleanup, code quality."
---

Finds unused and missing dependencies with depcheck: unused imports, missing deps, and configuration analysis.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx depcheck`, `npm uninstall unused-package`
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
