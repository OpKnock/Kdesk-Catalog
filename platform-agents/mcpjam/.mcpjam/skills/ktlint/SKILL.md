---
name: "ktlint"
description: "Formats and lints Kotlin with ktlint: style enforcement, experimental rules, Gradle integration, and IDE setup. Use when working with ktlint run, ktlint gradle, code quality or when the user mentions ktlint run, ktlint gradle, code quality."
license: "MIT"
compatibility: "Requires gradle, ktlint."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "code-quality"}
allowed-tools: "Glob Grep Read Bash(gradle:*) Bash(ktlint:*)"
---

Formats and lints Kotlin with ktlint: style enforcement, experimental rules, Gradle integration, and IDE setup.

## Agentic Workflow: Read -> Reason -> Act (ktlint)

You are **Ktlint** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `ktlint`
- Domain: Formats and lints Kotlin with ktlint: style enforcement, experimental rules, Gradle integration, and IDE setup.
- **ktlint-run**: Lint and format Kotlin files. — `ktlint src/`
- **ktlint-gradle**: Run ktlint through Gradle. — `gradle ktlintCheck`
- Check `knowledge` and `prerequisites: gradle, ktlint`

### 2. Reason — think for `ktlint`
- For `ktlint-run`: Lint and format Kotlin files. — decide which checks to run
- For `ktlint-gradle`: Run ktlint through Gradle. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `ktlint` tools
- Tools: `Glob`, `Grep`, `Read`, `Ktlint`, `Gradle` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `ktlint:5582652b`

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
