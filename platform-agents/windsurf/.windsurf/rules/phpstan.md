---
trigger: glob
description: "Run it analysis with level control, baselines, and CI output. legacy code. Use when working with phpstan analysis, code quality or when the user mentions phpstan analysis, code quality."
globs: ["**/*.json", "**/*.php", "**/*.r", "**/*.sh"]
---

Run it analysis with level control, baselines, and CI output. legacy code.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `vendor/bin/phpstan analyse src/`
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

# PHPStan

Finds bugs in PHP without running it: undefined variables, wrong types, and unsafe
calls, controlled by strictness levels 0-9.

## When to Use

- Catching type errors before deployment
- Raising analysis level incrementally on a mature codebase
- CI gate for PHP quality

## Real Commands

```bash
# Install
composer require --dev phpstan/phpstan

# Analyse with the configured level
vendor/bin/phpstan analyse src/

# Explicit level
vendor/bin/phpstan analyse -l 8 src/

# Legacy code: baseline current errors
vendor/bin/phpstan analyse --generate-baseline

# Then continue analysing with baseline loaded
vendor/bin/phpstan analyse src/

# CI-friendly output
vendor/bin/phpstan analyse --error-format=github src/

# Clear stale result cache after config changes
vendor/bin/phpstan clear-result-cache
```

## Config (phpstan.neon)

```neon
parameters:
  level: 8
  paths:
    - src
  excludePaths:
    - src/Generated
  ignoreErrors:
    - '#Undefined variable.*#i'
```

## Best Practices

- Start at level 5, raise one level per sprint
- Commit the generated baseline and shrink it deliberately
- Use `--memory-limit` in CI containers with low memory
- Add PHPStan to `composer.json` scripts: `"analyse": "phpstan analyse src/"`

## Example Response

Lists errors as `file:line` with rule names (e.g. 'Property is never read'), groups by
class, and suggests the config change or code fix.

## Capabilities

### phpstan-analysis
Run PHPStan analysis with level control, baselines, and CI output

**Parameters:**
- `level` (integer): Analysis strictness level 0-9 (or max)
- `error-format` (string): Output format: table, raw, json, github, checkstyle
- `generate-baseline` (boolean): Write current errors to phpstan-baseline.neon

**Commands:**
- `vendor/bin/phpstan analyse src/`
- `vendor/bin/phpstan analyse -l 8 src/`
- `vendor/bin/phpstan analyse --memory-limit=1G src tests`
- `vendor/bin/phpstan analyse --generate-baseline`
- `vendor/bin/phpstan clear-result-cache`

**Examples:**
- vendor/bin/phpstan analyse --level=max src/
- vendor/bin/phpstan analyse -c phpstan.neon --no-progress
- vendor/bin/phpstan analyse --error-format=github src/

## References
- [PHPStan docs](https://phpstan.org/)
- [PHPStan config reference](https://phpstan.org/config-reference)
