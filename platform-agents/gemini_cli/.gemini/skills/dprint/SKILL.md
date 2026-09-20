---
name: "dprint"
description: "Formats multiple languages with dprint, the fast pluggable formatter, including plugin config and CI integration."
---

# dprint

Formats multiple languages with dprint, the fast pluggable formatter, including plugin config and CI integration.

## Instructions

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

**Commands:**
- `dprint config add typescript`
- `dprint config add markdown`
- `dprint config update`
- `dprint output-resolved-config`

**Examples:**
- dprint config add "prettier:toml"
- dprint output-resolved-config > dprint-resolved.json
