---
trigger: glob
description: "Lints Python code with Pylint, enforcing style and catching bugs via a configurable rule system. Use when working with pylint linting, code quality or when the user mentions pylint linting, code quality."
globs: ["**/*.go", "**/*.json", "**/*.py", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

Lints Python code with Pylint, enforcing style and catching bugs via a configurable rule system.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `pylint src/`
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
