---
trigger: glob
description: "Format and verify files with it in write or check mode. for CI. Use when working with prettier formatting, code quality or when the user mentions prettier formatting, code quality."
globs: ["**/*.css", "**/*.go", "**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

Format and verify files with it in write or check mode. for CI.

## Agentic Workflow: Read -> Reason -> Act (prettier)

You are **prettier** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `prettier`
- Domain: Format and verify files with it in write or check mode. for CI.
- **prettier-formatting**: Format and verify files with Prettier in write or check mode — `npx prettier --write .`
- Check `knowledge` and `prerequisites: npx`

### 2. Reason — think for `prettier`
- For `prettier-formatting`: Format and verify files with Prettier in write or check mode — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `prettier` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `prettier:6f9f87ab`

# Prettier

Opinionated code formatter for JS/TS/CSS/JSON/Markdown with a strict check mode
for CI.

## When to Use

- Standardizing formatting across a team
- Enforcing formatting in CI without write access
- One-time formatting of a legacy codebase

## Real Commands

```bash
# Format everything
npx prettier --write .

# Check mode (CI): fails if anything is unformatted
npx prettier --check .

# Format only TS/TSX in src
npx prettier "src/**/*.{ts,tsx}" --write

# List files that need formatting
npx prettier --list-different .

# Dry-run via stdout only
npx prettier src/app.ts

# With custom options
npx prettier --write --single-quote --trailing-comma all src/
```

## Ignore Files (.prettierignore)

```
dist/
build/
package-lock.json
*.min.js
```

## CI

```yaml
- name: Format check
  run: npx prettier --check . --ignore-path .prettierignore
```

## Integration

- ESLint: use `eslint-plugin-prettier` or run Prettier after ESLint
- Pre-commit: `npx prettier --write` on staged files via lint-staged
- Editor: enable format-on-save with the Prettier extension

## Best Practices

- Never mix Prettier with other formatters (black, gofmt) on the same files
- Run `--write` before `--check` in migration; then enforce check in CI
- Keep `.prettierignore` in sync with `.gitignore`
- Pin the Prettier major version to avoid churn

## Capabilities

### prettier-formatting
Format and verify files with Prettier in write or check mode

**Parameters:**
- `write` (boolean): Rewrite files in place; without it, only print to stdout
- `check` (boolean): Verify formatting, exit 1 if files need formatting
- `list-different` (boolean): Print file names that differ from Prettier output

**Commands:**
- `npx prettier --write .`
- `npx prettier --check src/`
- `npx prettier "src/**/*.{ts,tsx}" --write`
- `npx prettier --list-different "**/*.{js,json,md}"`
- `npx prettier --debug-check src/index.ts`

**Examples:**
- npx prettier --check . --ignore-path .prettierignore
- npx prettier --write package.json README.md
- npx prettier --plugin=prettier-plugin-organize-imports --write src/

## References
- [Prettier docs](https://prettier.io/docs/en/)
- [Prettier CLI reference](https://prettier.io/docs/en/cli.html)
