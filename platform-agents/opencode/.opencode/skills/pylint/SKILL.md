---
name: "pylint"
description: "Lints Python code with Pylint, enforcing style and catching bugs via a configurable rule system. Use when working with pylint linting, code quality or when the user mentions pylint linting, code quality."
---

Lints Python code with Pylint, enforcing style and catching bugs via a configurable rule system.

## Agentic Workflow: Read -> Reason -> Act (pylint)

You are **pylint** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `pylint`
- Domain: Lints Python code with Pylint, enforcing style and catching bugs via a configurable rule system.
- **pylint-linting**: Run Pylint with custom rc files, score thresholds, and CI formats — `pylint src/`
- Check `knowledge` and `prerequisites: pylint`

### 2. Reason — think for `pylint`
- For `pylint-linting`: Run Pylint with custom rc files, score thresholds, and CI formats — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `pylint` tools
- Tools: `Glob`, `Grep`, `Read`, `Pylint` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `pylint:a2e774d3`

# Pylint

Checks Python code for errors, style problems, and design smells, scoring each
module on a 0-10 scale.

## When to Use

- Enforcing style and naming conventions
- Catching unused imports, undefined vars, and bad redefinitions
- Gatekeeping merge requests with a minimum score

## Real Commands

```bash
# Install
pip install pylint

# Basic run
pylint src/

# Generate a config file
pylint --generate-rcfile > .pylintrc

# Use the config with a score gate
pylint --rcfile=.pylintrc --fail-under=9 src/

# Errors only
pylint --errors-only src/

# JSON for CI
pylint --output-format=json src/ > pylint-report.json

# Disable specific checks inline
pylint --disable=too-many-locals,too-many-branches src/
```

## Config (.pylintrc)

```ini
[MESSAGES CONTROL]
disable=missing-docstring,too-many-arguments,invalid-name

[MASTER]
fail-under=9
load-plugins=pylint.extensions.docparams
```

## CI

```yaml
- name: Pylint
  run: pylint --rcfile=.pylintrc --fail-under=9 src/
```

## Best Practices

- Commit a generated `.pylintrc`; don't rely on defaults
- Set `fail-under` a bit below a perfect score so regressions fail but noise is allowed
- Keep `--disable` lists small and reviewed
- Use `# pylint: disable=...` inline comments sparingly

## Example Response

Reports per-module scores, message counts by category (E/W/R/C), and the worst
offenders with `file:line` references.

## Capabilities

### pylint-linting
Run Pylint with custom rc files, score thresholds, and CI formats

**Parameters:**
- `fail-under` (number): Exit non-zero if the final score is below this value
- `output-format` (string): text, colorized, json, parseable, or sarif
- `rcfile` (string): Configuration file to use

**Commands:**
- `pylint src/`
- `pylint --rcfile=.pylintrc app tests`
- `pylint --fail-under=9 src/`
- `pylint --output-format=json src/ > pylint.json`
- `pylint --disable=missing-docstring,too-many-arguments src/`

**Examples:**
- pylint --generate-rcfile > .pylintrc
- pylint --fail-under=9 --reports=y src/
- pylint --errors-only src/

## References
- [Pylint docs](https://pylint.readthedocs.io/)
- [Pylint message codes](https://pylint.readthedocs.io/en/stable/technical_reference/features.html)
