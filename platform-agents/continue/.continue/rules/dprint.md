---
name: "dprint"
description: "Formats multiple languages with dprint, the fast pluggable formatter, including plugin config and CI integration. Use when working with dprint format, dprint config, code quality or when the user mentions dprint format, dprint config, code quality."
globs: ["**/*.json", "**/*.r", "**/*.sh", "**/*.{ts,tsx}"]
alwaysApply: false
---

Formats multiple languages with dprint, the fast pluggable formatter, including plugin config and CI integration.

## Agentic Workflow: Read -> Reason -> Act (dprint)

You are **dprint** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `dprint`
- Domain: Formats multiple languages with dprint, the fast pluggable formatter, including plugin config and CI integration.
- **dprint-format**: Format code with dprint plugins. — `npm install -g dprint`
- **dprint-config**: Manage plugins and configuration. — `dprint config add typescript`
- Check `knowledge` and `prerequisites: dprint, npm`

### 2. Reason — think for `dprint`
- For `dprint-format`: Format code with dprint plugins. — decide which checks to run
- For `dprint-config`: Manage plugins and configuration. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `dprint` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Dprint` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `dprint:5c094be4`

# dprint

Fast, pluggable code formatter.

## When to Use

- Formatting many languages with one tool
- Replacing slower formatters on large repos
- Enforcing formatting in CI cheaply
- Standardizing team-wide formatting rules

## Commands

```bash
# Install and init
npm install -g dprint
dprint init

# Format
dprint fmt
dprint fmt --include "**/*.ts"
dprint fmt --exclude "**/dist/**"

# Check (CI)
dprint check

# Config
dprint config add typescript
dprint config add markdown
dprint config add "prettier:toml"
dprint config update
dprint output-resolved-config
```

## Config Example

```json
{
  "typescript": {
    "lineWidth": 100,
    "semiColons": "always"
  },
  "markdown": {},
  "includes": ["**/*.{ts,tsx,json,md}"],
  "excludes": ["**/dist/**", "**/node_modules/**"]
}
```

## Best Practices

- Commit dprint.json at the repo root
- Run dprint check in CI, dprint fmt in pre-commit
- Use only the plugins your repo needs
- Keep the dprint binary version pinned
- Exclude generated directories from formatting
- Resolve config in CI with output-resolved-config to debug drift

## Capabilities

### dprint-format
Format code with dprint plugins.

**Parameters:**
- `paths` (string): Paths or globs
- `check` (boolean): Verify without writing

**Commands:**
- `npm install -g dprint`
- `dprint init`
- `dprint fmt`
- `dprint check`
- `dprint fmt --include "**/*.ts"`

**Examples:**
- dprint check ./src
- dprint fmt --exclude "**/dist/**"
- dprint fmt -- --stdin-filepath main.ts

### dprint-config
Manage plugins and configuration.

**Parameters:**
- `plugin` (string): Plugin name
- `version` (string): Plugin version to pin

**Commands:**
- `dprint config add typescript`
- `dprint config add markdown`
- `dprint config update`
- `dprint output-resolved-config`

**Examples:**
- dprint config add "prettier:toml"
- dprint output-resolved-config > dprint-resolved.json

## References
- [dprint Docs](https://dprint.dev)
- [dprint on GitHub](https://github.com/dprint/dprint)