---
name: "markdownlint"
description: "Lints Markdown files with markdownlint/markdownlint-cli2, enforcing consistent heading, list, and link style."
globs: ["**/*.html", "**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
alwaysApply: false
---

# markdownlint

Lints Markdown files with markdownlint/markdownlint-cli2, enforcing consistent heading, list, and link style.

## Instructions

# Markdownlint

Lints Markdown files against a rule set covering headings, lists, indentation, links,
and code fences so documentation stays consistent.

## When to Use

- Enforcing consistent docs style in a repo
- Catching broken link syntax or mixed list markers in README files
- Pre-commit/CI checks for markdown

## Real Commands

```bash
# Check one file
npx markdownlint-cli2 README.md

# Check all markdown in docs/, ignoring node_modules and vendor
npx markdownlint-cli2 'docs/**/*.md' '#node_modules' '#vendor'

# Auto-fix
npx markdownlint-cli2 --fix 'docs/**/*.md'

# Custom config
npx markdownlint-cli2 --config .markdownlint-cli2.yaml .

# JSON report for CI
npx markdownlint-cli2 --output report.json '**/*.md' '#node_modules'
```

## Config (.markdownlint-cli2.yaml)

```yaml
config:
  MD013:
    line_length: 100
  MD024: false
  MD033: false
ignores:
  - 'node_modules/**'
```

## CI

```yaml
- name: Lint docs
  run: npx markdownlint-cli2 '**/*.md' '#node_modules' '#dist'
```

## Best Practices

- Use glob ignores (`#node_modules`) rather than editing files
- Disable rules deliberately (MD013 long lines, MD033 inline HTML) per team taste
- Run `--fix` before review, then address remaining warnings manually
- Check config is committed so CI matches local behavior

## Capabilities

### markdown-linting
Check and fix Markdown style violations with configurable rule sets

**Commands:**
- `npx markdownlint-cli2 'docs/**/*.md'`
- `npx markdownlint-cli2 --fix .`
- `npx markdownlint-cli2 --config .markdownlint-cli2.yaml README.md`
- `npx markdownlint-cli2 '**/*.md' '#node_modules' '#vendor'`
- `npx markdownlint-cli2 --output markdownlint-report.json '**/*.md'`

**Examples:**
- npx markdownlint-cli2 --fix docs/
- npx markdownlint-cli2 README.md CHANGELOG.md
- npx markdownlint-cli2 '**/*.md' --config .markdownlint-cli2.yaml