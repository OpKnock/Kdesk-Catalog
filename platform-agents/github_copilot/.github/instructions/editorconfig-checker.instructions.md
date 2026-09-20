---
applyTo: "**/*.go **/*.r **/*.sh"
---

# editorconfig-checker

Verifies files comply with .editorconfig rules using editorconfig-checker in local and CI workflows.

## Instructions

# editorconfig-checker

Enforce editor conventions across the repo.

## When to Use

- Ensuring consistent indentation and line endings
- Enforcing charset and end-of-line rules repo-wide
- CI gates on .editorconfig compliance
- Catching files created by Windows/macOS editors

## .editorconfig Example

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
indent_style = space
indent_size = 2
trim_trailing_whitespace = true
insert_final_newline = true

[*.py]
indent_size = 4
```

## Commands

```bash
# Install
go install github.com/editorconfig-checker/editorconfig-checker/cmd/editorconfig-checker@latest
# or
npx editorconfig-checker

# Check the repo
editorconfig-checker

# Exclude paths
editorconfig-checker -exclude "**/vendor/**,dist/**"

# Custom config
editorconfig-checker -config .eccrc

# Verbose/debug
editorconfig-checker -verbose
editorconfig-checker -debug
```

## Best Practices

- Define root = true and per-extension rules
- Run editorconfig-checker in pre-commit and CI
- Exclude generated and vendored directories
- Pair with a formatter for the actual file writes
- Commit .editorconfig so editors adopt it automatically

## Capabilities

### ecc-check
Check files against .editorconfig.

**Commands:**
- `editorconfig-checker`
- `editorconfig-checker -exclude "**/vendor/**"`
- `editorconfig-checker -config .eccrc`
- `editorconfig-checker file.txt`
- `editorconfig-checker -version`

**Examples:**
- editorconfig-checker -exclude "dist/**"
- editorconfig-checker -no-color
- editorconfig-checker -verbose

### ecc-config
Manage .editorconfig and checker config.

**Commands:**
- `editorconfig-checker -help`
- `editorconfig-checker -debug`
- `npx editorconfig-checker`
- `editorconfig-checker -disable-indent-size`

**Examples:**
- npx editorconfig-checker -exclude "**/node_modules/**"
- editorconfig-checker -disable-max-line-length
