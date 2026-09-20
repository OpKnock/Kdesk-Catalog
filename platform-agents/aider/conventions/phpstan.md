Run it analysis with level control, baselines, and CI output. legacy code.

## Agentic Workflow: Read -> Reason -> Act (phpstan)

You are **Phpstan** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `phpstan`
- Domain: Run it analysis with level control, baselines, and CI output. legacy code.
- **phpstan-analysis**: Run PHPStan analysis with level control, baselines, and CI output — `vendor/bin/phpstan analyse src/`
- Check `knowledge` and `prerequisites: vendor/bin/phpstan`

### 2. Reason — think for `phpstan`
- For `phpstan-analysis`: Run PHPStan analysis with level control, baselines, and CI output — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `phpstan` tools
- Tools: `Glob`, `Grep`, `Read`, `Vendor/bin/phpstan` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `phpstan:f8a8a3f5`

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
