---
trigger: glob
description: "Finds bugs and security issues with Semgrep's pattern-based SAST across 30+ languages, including custom rules and CI integration. Use when working with semgrep scan, custom rules, ci integration, security or when the user mentions semgrep scan, custom rules, ci integration, security."
globs: ["**/*.json", "**/*.py", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

Finds bugs and security issues with Semgrep's pattern-based SAST across 30+ languages, including custom rules and CI integration.

## Agentic Workflow: Read -> Reason -> Act (semgrep)

You are **semgrep** (security/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — security context for `semgrep`
- Domain: Finds bugs and security issues with Semgrep's pattern-based SAST across 30+ languages, including custom rules and CI integration.
- **semgrep-scan**: Scan code with built-in or custom rule packs. — `semgrep scan --config auto .`
- **custom-rules**: Write and test custom pattern rules. — `semgrep scan --config custom.yml .`
- **ci-integration**: Run Semgrep CI with findings management. — `semgrep login`
- Check `knowledge` and `prerequisites: semgrep`

### 2. Reason — think for `semgrep`
- For `semgrep-scan`: Scan code with built-in or custom rule packs. — decide which checks to run
- For `custom-rules`: Write and test custom pattern rules. — decide which checks to run
- For `ci-integration`: Run Semgrep CI with findings management. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `semgrep` tools
- Tools: `Glob`, `Grep`, `Read`, `Semgrep` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `semgrep:62704b03`

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

**Parameters:**
- `config` (string): Ruleset: auto, p/..., local YAML file
- `severity` (string): Minimum severity: ERROR, WARNING, INFO
- `jsonOutput` (string): Path to write JSON results

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

**Parameters:**
- `pattern` (string): Inline match pattern
- `lang` (string): Language for inline patterns

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

**Parameters:**
- `sarif` (boolean): Output SARIF format
- `supplyChain` (boolean): Enable supply-chain dependency scanning

**Commands:**
- `semgrep login`
- `semgrep ci`
- `semgrep ci --json -o results.sarif --sarif`
- `semgrep ci --supply-chain`

**Examples:**
- semgrep ci
- semgrep ci --sarif -o results.sarif
- semgrep ci --supply-chain

## References
- [Semgrep Documentation](https://semgrep.dev/docs/)
- [Semgrep Registry](https://semgrep.dev/r)
