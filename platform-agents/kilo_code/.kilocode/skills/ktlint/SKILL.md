---
name: "ktlint"
description: "Formats and lints Kotlin with ktlint: style enforcement, experimental rules, Gradle integration, and IDE setup. Use when working with ktlint run, ktlint gradle, code quality or when the user mentions ktlint run, ktlint gradle, code quality."
license: "MIT"
compatibility: "Requires gradle, ktlint."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "code-quality"}
allowed-tools: "Glob Grep Read Bash(gradle:*) Bash(ktlint:*)"
---

Formats and lints Kotlin with ktlint: style enforcement, experimental rules, Gradle integration, and IDE setup.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `ktlint src/`, `gradle ktlintCheck`
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

# ktlint

Kotlin linter and formatter.

## When to Use

- Enforcing the official Kotlin style guide
- Auto-formatting Kotlin in pre-commit
- CI checks for style drift
- Android and multiplatform projects

## Commands

```bash
# Lint
ktlint src/
ktlint "src/**/*.kt"

# Auto-format
ktlint --format src/

# Experimental rules
ktlint --experimental src/
ktlint --format --experimental src/

# Android conventions
ktlint --android src/

# Reports
ktlint --reporter=json --output=report.json

# Gradle
gradle ktlintCheck
gradle ktlintFormat
gradle ktlintGenerateBaseline
```

## Config Example

```yaml
# .editorconfig
[*.{kt,kts}]
ktlint_standard_max-line-length = 120
ktlint_experimental = enabled
```

## Best Practices

- Run ktlint --format locally, ktlintCheck in CI
- Generate a baseline when adopting on legacy code
- Enable experimental rules only when team-agreed
- Keep editorconfig as the single source of settings
- Pair with detekt for deeper analysis
- Format before linting for stable results

## Capabilities

### ktlint-run
Lint and format Kotlin files.

**Parameters:**
- `paths` (string): Files or directories
- `format` (boolean): Auto-format
- `experimental` (boolean): Enable experimental rules

**Commands:**
- `ktlint src/`
- `ktlint --format src/`
- `ktlint --experimental src/`
- `ktlint "src/**/*.kt"`
- `ktlint --verbose src/Main.kt`

**Examples:**
- ktlint --format --experimental src/
- ktlint --reporter=json --output=report.json
- ktlint --android src/

### ktlint-gradle
Run ktlint through Gradle.

**Parameters:**
- `baseline` (string): Baseline file path
- `android` (boolean): Apply Android-specific conventions

**Commands:**
- `gradle ktlintCheck`
- `gradle ktlintFormat`
- `gradle ktlintGenerateBaseline`
- `gradle ktlintApplyToIDEA`

**Examples:**
- gradle ktlintCheck --continue
- gradle ktlintFormat -PktlintExperimental=true

## References
- [ktlint Docs](https://pinterest.github.io/ktlint/)
- [Kotlin Official Style Guide](https://kotlinlang.org/docs/coding-conventions.html)
