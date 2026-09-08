---
trigger: glob
description: "Run it from the command line or Gradle. Manage existing debt with baselines. and Gradle integration.'. Use when working with detekt cli, detekt baseline, code quality or when the user mentions detekt cli, detekt baseline, code quality."
globs: ["**/*.kt", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

Run it from the command line or Gradle. Manage existing debt with baselines. and Gradle integration.'

## Agentic Workflow: Read -> Reason -> Act (detekt)

You are **Detekt** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `detekt`
- Domain: Run it from the command line or Gradle. Manage existing debt with baselines. and Gradle integration.'
- **detekt-cli**: Run detekt from the command line or Gradle. — `detekt --input src/main/kotlin`
- **detekt-baseline**: Manage existing debt with baselines. — `detekt --baseline detekt-baseline.xml --input src/`
- Check `knowledge` and `prerequisites: detekt, gradle`

### 2. Reason — think for `detekt`
- For `detekt-cli`: Run detekt from the command line or Gradle. — decide which checks to run
- For `detekt-baseline`: Manage existing debt with baselines. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `detekt` tools
- Tools: `Glob`, `Grep`, `Read`, `Detekt`, `Gradle` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `detekt:46eb961d`

# detekt

Static analysis for Kotlin.

## When to Use

- Enforcing Kotlin style and complexity budgets
- Catching smells (long methods, magic numbers, duplicates)
- Kotlin codebases using Gradle
- CI quality gates

## Commands

```bash
# CLI
detekt --input src/main/kotlin
detekt --config detekt.yml --input src/

# Reports
detekt --report xml:detekt-report.xml
detekt --report sarif:detekt-report.sarif

# Gradle
gradle detekt
gradle detektMain detektTest

# Baseline (accept existing findings)
gradle detektBaseline
detekt --baseline detekt-baseline.xml

# Generate default config
detekt --generate-config --config detekt.yml
```

## Config Example

```yaml
# detekt.yml
complexity:
  LongMethod:
    threshold: 60
  TooManyFunctions:
    thresholdInFiles: 12

style:
  MagicNumber:
    ignoreNumbers: ['-1', '0', '1', '2']
```

## Best Practices

- Keep the default rule set; enable extensions deliberately
- Use baselines to adopt detekt on legacy code
- Regenerate baseline only on reviewed improvements
- Fail CI on new violations, allow old baselined ones
- Integrate with Gradle: gradle detekt --continue
- Pair with ktlint for formatting concerns

## Capabilities

### detekt-cli
Run detekt from the command line or Gradle.

**Parameters:**
- `input` (string): Source directory
- `config` (string): Config yaml path
- `baseline` (string): Baseline xml path

**Commands:**
- `detekt --input src/main/kotlin`
- `detekt --config detekt.yml --input src/`
- `gradle detekt`
- `gradle detektMain detektTest`
- `detekt --version`

**Examples:**
- detekt --input src/ --report xml:detekt-report.xml
- detekt --baseline detekt-baseline.xml
- gradle detekt --continue

### detekt-baseline
Manage existing debt with baselines.

**Parameters:**
- `generate-config` (boolean): Generate default config
- `input` (string): Source directory to scan

**Commands:**
- `detekt --baseline detekt-baseline.xml --input src/`
- `detekt --build-upon-default-config`
- `gradle detektBaseline`
- `detekt --generate-config`

**Examples:**
- gradle detektBaseline && gradle detekt
- detekt --generate-config --config detekt.yml

## References
- [detekt Docs](https://detekt.dev)
- [detekt on GitHub](https://github.com/detekt/detekt)
