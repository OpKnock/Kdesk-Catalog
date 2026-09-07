---
name: "code-formatting"
description: "Applies consistent code formatting across languages with prettier, black, gofmt, rustfmt, and formatter configurations. Use when working with prettier format, language formatters, code quality or when the user mentions prettier format, language formatters, code quality."
license: "MIT"
compatibility: "Requires black, cargo, gofmt, npx, rustfmt."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "code-quality"}
allowed-tools: "Glob Grep Read Bash(black:*) Bash(cargo:*) Bash(go:*) Bash(gofmt:*) Bash(npx:*) Bash(rustfmt:*)"
---

Applies consistent code formatting across languages with prettier, black, gofmt, rustfmt, and formatter configurations.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx prettier --write src/`, `black src/`
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
