---
name: "detekt"
description: "Run it from the command line or Gradle. Manage existing debt with baselines. and Gradle integration.'. Use when working with detekt cli, detekt baseline, code quality or when the user mentions detekt cli, detekt baseline, code quality."
license: "MIT"
compatibility: "Requires detekt, gradle."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "code-quality"}
allowed-tools: "Glob Grep Read Bash(detekt:*) Bash(gradle:*)"
---

Run it from the command line or Gradle. Manage existing debt with baselines. and Gradle integration.'

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `detekt --input src/main/kotlin`, `detekt --baseline detekt-baseline.xml --input src/`
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
