---
trigger: glob
description: "Format and verify files with it in write or check mode. for CI. Use when working with prettier formatting, code quality or when the user mentions prettier formatting, code quality."
globs: ["**/*.css", "**/*.go", "**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

Format and verify files with it in write or check mode. for CI.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx prettier --write .`
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
