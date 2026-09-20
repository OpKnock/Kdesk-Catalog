---
name: "code-formatting"
description: "Applies consistent code formatting across languages with prettier, black, gofmt, rustfmt, and formatter configurations."
type: knowledge
triggers: ["code-formatting", "prettier-format", "language-formatters"]
---

# code-formatting

Applies consistent code formatting across languages with prettier, black, gofmt, rustfmt, and formatter configurations.

## Instructions

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
