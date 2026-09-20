---
name: "semgrep"
description: "Finds bugs and security issues with Semgrep's pattern-based SAST across 30+ languages, including custom rules and CI integration."
type: knowledge
triggers: ["semgrep", "semgrep-scan", "custom-rules", "ci-integration"]
---

# semgrep

Finds bugs and security issues with Semgrep's pattern-based SAST across 30+ languages, including custom rules and CI integration.

## Instructions

# Semgrep

Fast, pattern-based static analysis with first-class custom rule support.

## What This Skill Does

- Scans 30+ languages with rules matching code structure, not just regex
- Runs OWASP Top 10 and language-specific rule packs
- Authors custom rules with metavariables and pattern composition
- Emits SARIF/JSON for CI and code scanning

## When to Use

- Finding security bugs in large monorepos fast
- Enforcing team-specific code patterns
- Replacing regex greps with maintainable rules

## Real Commands

```bash
# Standard scans
semgrep scan --config auto .
semgrep scan --config p/owasp-top-ten .
semgrep scan --config p/python --severity ERROR src/

# Inline pattern
semgrep scan --pattern 'eval($X)' --lang python .

# Custom rules
semgrep scan --config custom.yml .
semgrep scan --validate --config custom.yml

# CI
semgrep login
semgrep ci --sarif -o results.sarif
semgrep ci --supply-chain
```

## Custom Rule

```yaml
rules:
  - id: no-exec-user-input
    patterns:
      - pattern: exec($CODE)
      - pattern-not: exec("fixed-command")
    message: Avoid exec with dynamic input
    languages: [python]
    severity: ERROR
```

## Best Practices

- Run --config auto locally, p/ rules for language depth
- Validate custom rules in CI with --validate
- Use SARIF for inline GitHub annotations
- Fix findings at the source; track false positives with nosemgrep
- Run semgrep ci to correlate findings across PRs

## Capabilities

### semgrep-scan
Scan code with built-in or custom rule packs.

**Commands:**
- `semgrep scan --config auto .`
- `semgrep scan --config p/owasp-top-ten .`
- `semgrep scan --config p/python .`
- `semgrep scan --config rules.yml src/`
- `semgrep scan --config auto --severity ERROR --json -o results.json`

**Examples:**
- semgrep scan --config auto .
- semgrep scan --config p/owasp-top-ten .
- semgrep scan --config p/python --severity ERROR src/

### custom-rules
Write and test custom pattern rules.

**Commands:**
- `semgrep scan --config custom.yml .`
- `semgrep scan --validate --config custom.yml`
- `semgrep scan --config semgrep-rules/ --dry-run`
- `semgrep scan --pattern 'eval($X)' --lang python .`

**Examples:**
- semgrep scan --validate --config custom.yml
- semgrep scan --pattern 'exec($X)' --lang python .
- semgrep scan --config semgrep-rules/ .

### ci-integration
Run Semgrep CI with findings management.

**Commands:**
- `semgrep login`
- `semgrep ci`
- `semgrep ci --json -o results.sarif --sarif`
- `semgrep ci --supply-chain`

**Examples:**
- semgrep ci
- semgrep ci --sarif -o results.sarif
- semgrep ci --supply-chain
