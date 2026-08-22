# biome

Formats and lints JavaScript/TypeScript with Biome, the fast Rust-based toolchain, including migrate from ESLint/Prettier.

## Instructions

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

**Commands:**
- `npx @biomejs/biome migrate eslint`
- `npx @biomejs/biome migrate prettier`
- `npx @biomejs/biome migrate --write`
- `npx @biomejs/biome rage`

**Examples:**
- npx @biomejs/biome migrate eslint --write
- npx @biomejs/biome rage --config
