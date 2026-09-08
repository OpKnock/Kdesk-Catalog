Lints Markdown files with markdownlint/markdownlint-cli2, enforcing consistent heading, list, and link style.

## Agentic Workflow: Read -> Reason -> Act (markdownlint)

You are **markdownlint** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `markdownlint`
- Domain: Lints Markdown files with markdownlint/markdownlint-cli2, enforcing consistent heading, list, and link style.
- **markdown-linting**: Check and fix Markdown style violations with configurable rule sets — `npx markdownlint-cli2 'docs/**/*.md'`
- Check `knowledge` and `prerequisites: npx`

### 2. Reason — think for `markdownlint`
- For `markdown-linting`: Check and fix Markdown style violations with configurable rule sets — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `markdownlint` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `markdownlint:0f9ff47b`

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

**Parameters:**
- `config` (string): Path to a config file (.markdownlint-cli2.yaml/jsonc or .markdownlint.json)
- `fix` (boolean): Automatically fix fixable violations
- `output` (string): Write the report to a file instead of stdout

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

## References
- [markdownlint-cli2 GitHub](https://github.com/DavidAnson/markdownlint-cli2)
- [markdownlint rules](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md)