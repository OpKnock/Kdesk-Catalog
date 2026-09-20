---
trigger: glob
description: "Applies consistent code formatting across languages with prettier, black, gofmt, rustfmt, and formatter configurations. Use when working with prettier format, language formatters, code quality or when the user mentions prettier format, language formatters, code quality."
globs: ["**/*.css", "**/*.go", "**/*.html", "**/*.json", "**/*.py", "**/*.r", "**/*.rs", "**/*.sh", "**/*.{yaml,yml}"]
---

Applies consistent code formatting across languages with prettier, black, gofmt, rustfmt, and formatter configurations.

## Agentic Workflow: Read -> Reason -> Act (code-formatting)

You are **code-formatting** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `code-formatting`
- Domain: Applies consistent code formatting across languages with prettier, black, gofmt, rustfmt, and formatter configurations.
- **prettier-format**: Format JS/TS/HTML/CSS/MD with Prettier. — `npx prettier --write src/`
- **language-formatters**: Format Python, Go, and Rust. — `black src/`
- Check `knowledge` and `prerequisites: black, cargo, gofmt, npx`

### 2. Reason — think for `code-formatting`
- For `prettier-format`: Format JS/TS/HTML/CSS/MD with Prettier. — decide which checks to run
- For `language-formatters`: Format Python, Go, and Rust. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `code-formatting` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx`, `Black` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `code-formatting:672cc44f`

# Code Formatting

Enforce one formatting style across the repo.

## When to Use

- Every codebase with more than one contributor
- Ending style arguments with config, not discussion
- Pre-commit and CI formatting gates
- Language-agnostic consistency (configs, markdown, YAML)

## Commands

```bash
# Prettier (JS/TS/CSS/HTML/MD/JSON)
npx prettier --write src/
npx prettier --check src/
npx prettier --write "src/**/*.{ts,tsx}"

# Python
black src/
black --check src/

# Go
gofmt -w ./
gofmt -l .

# Rust
cargo fmt --all
rustfmt --check src/
```

## Prettier Config

```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "printWidth": 100,
  "trailingComma": "all"
}
```

## Best Practices

- Commit the formatter config at the repo root
- Use --check in CI, --write in pre-commit
- Let formatters handle style; reviewers handle logic
- Format generated files with ignore directives
- Keep formatter versions pinned to avoid churn
- Run formatting before linting for stable error lines

## Capabilities

### prettier-format
Format JS/TS/HTML/CSS/MD with Prettier.

**Parameters:**
- `paths` (string): Files or globs
- `check` (boolean): Verify without writing
- `tab-width` (integer): Indent width

**Commands:**
- `npx prettier --write src/`
- `npx prettier --check src/`
- `npx prettier --write "src/**/*.{ts,tsx}"`
- `npx prettier --config .prettierrc --write .`
- `npx prettier --write --single-quote src/`

**Examples:**
- npx prettier --check .
- npx prettier --write . --tab-width 2
- npx prettier --write --prose-wrap always README.md

### language-formatters
Format Python, Go, and Rust.

**Parameters:**
- `language` (string): python, go, rust
- `config` (string): Formatter config path

**Commands:**
- `black src/`
- `gofmt -w ./`
- `go fmt ./...`
- `rustfmt --check src/`
- `cargo fmt --all`

**Examples:**
- gofmt -l .
- rustfmt --edition 2021 src/main.rs
- cargo fmt --all -- --check

## References
- [Prettier Docs](https://prettier.io/docs/)
- [gofmt Docs](https://pkg.go.dev/cmd/gofmt)
- [Rustfmt Docs](https://rust-lang.github.io/rustfmt/)
