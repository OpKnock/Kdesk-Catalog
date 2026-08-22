---
name: "Ktlint"
description: "Formats and lints Kotlin with ktlint: style enforcement, experimental rules, Gradle integration, and IDE setup."
globs: ["**/*.json", "**/*.kt", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
alwaysApply: false
---

# Ktlint

Formats and lints Kotlin with ktlint: style enforcement, experimental rules, Gradle integration, and IDE setup.

## Instructions

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

**Commands:**
- `gradle ktlintCheck`
- `gradle ktlintFormat`
- `gradle ktlintGenerateBaseline`
- `gradle ktlintApplyToIDEA`

**Examples:**
- gradle ktlintCheck --continue
- gradle ktlintFormat -PktlintExperimental=true