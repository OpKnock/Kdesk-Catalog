---
name: "biome"
description: "Formats and lints JavaScript/TypeScript with Biome, the fast Rust-based toolchain, including migrate from ESLint/Prettier. Use when working with biome cli, biome migrate, code quality or when the user mentions biome cli, biome migrate, code quality."
---

Formats and lints JavaScript/TypeScript with Biome, the fast Rust-based toolchain, including migrate from ESLint/Prettier.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx @biomejs/biome init`, `npx @biomejs/biome migrate eslint`
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

# Biome

Fast JS/TS formatter and linter in one tool.

## When to Use

- Replacing ESLint + Prettier with a single fast tool
- New projects wanting zero-config defaults
- Large repos where lint speed matters
- Enforcing consistent formatting in CI

## Commands

```bash
# Init
npx @biomejs/biome init

# Check (lint + format)
npx @biomejs/biome check src/
npx @biomejs/biome check --write src/

# Format only
npx @biomejs/biome format --write src/

# Lint only
npx @biomejs/biome lint src/

# Migrate from ESLint/Prettier
npx @biomejs/biome migrate eslint --write
npx @biomejs/biome migrate prettier

# Diagnostics
npx @biomejs/biome rage
```

## Config Example

```json
{
  "$schema": "./node_modules/@biomejs/biome/configuration_schema.json",
  "formatter": { "indentStyle": "space", "indentWidth": 2 },
  "linter": {
    "rules": {
      "recommended": true,
      "suspicious": { "noExplicitAny": "warn" }
    }
  }
}
```

## Best Practices

- Use check --write in pre-commit, verify-only in CI
- Keep the generated schema reference in biome.json
- Run biome migrate when adopting from legacy configs
- Scope rules per directory with overrides if needed
- Treat lint errors as CI failures; use warns sparingly
- Leverage --staged for fast pre-commit runs

## Capabilities

### biome-cli
Lint, format, and check code with Biome.

**Parameters:**
- `paths` (string): Files or dirs to check
- `write` (boolean): Apply fixes
- `staged` (boolean): Check staged files only

**Commands:**
- `npx @biomejs/biome init`
- `npx @biomejs/biome check src/`
- `npx @biomejs/biome check --write src/`
- `npx @biomejs/biome format --write src/`
- `npx @biomejs/biome lint src/`

**Examples:**
- npx @biomejs/biome check --apply src/
- npx @biomejs/biome format --write --indent-style=space src/
- npx @biomejs/biome check --staged

### biome-migrate
Migrate from ESLint and Prettier configs.

**Parameters:**
- `from` (string): eslint or prettier
- `write` (boolean): Write the migrated config to disk

**Commands:**
- `npx @biomejs/biome migrate eslint`
- `npx @biomejs/biome migrate prettier`
- `npx @biomejs/biome migrate --write`
- `npx @biomejs/biome rage`

**Examples:**
- npx @biomejs/biome migrate eslint --write
- npx @biomejs/biome rage --config

## References
- [Biome Docs](https://biomejs.dev)
- [Biome Migrate](https://biomejs.dev/recipes/migrate-eslint-prettier/)
