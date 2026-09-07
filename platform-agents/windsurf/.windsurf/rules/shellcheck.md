---
trigger: glob
description: "Finds bugs and portability issues in shell scripts with ShellCheck, including CI and JSON output. Use when working with shellcheck, code quality or when the user mentions shellcheck, code quality."
globs: ["**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

Finds bugs and portability issues in shell scripts with ShellCheck, including CI and JSON output.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `shellcheck script.sh`
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

# ShellCheck

Static analysis for shell scripts: quoting bugs, unportable syntax, and undefined
variable misuse.

## When to Use

- Reviewing CI scripts, deploy scripts, and init scripts
- Enforcing shell hygiene across a repo
- Catching quote bugs that fail only at runtime

## Real Commands

```bash
# Install (apt/brew)
sudo apt install shellcheck

# Check one script
shellcheck deploy.sh

# Follow sourced files with -x
shellcheck -x scripts/*.sh

# Only warnings and above
shellcheck --severity=warning scripts/

# Ignore specific codes (e.g. SC2086 unquoted vars you accept)
shellcheck -e SC2086,SC1091 scripts/start.sh

# JSON output for dashboards
shellcheck --format=json scripts/ > shellcheck-report.json

# gcc-format for editor integration
shellcheck --format=gcc scripts/*.sh
```

## CI

```yaml
- name: ShellCheck
  run: shellcheck --severity=warning --exclude=SC1091 scripts/*.sh
```

## Best Practices

- Always quote variable expansions (`"$var"`) - SC2086
- Use `[[ ]]` instead of `[ ]` in bash scripts
- Add `set -euo pipefail` at the top of every script
- Exclude codes with a comment, never silently: `# shellcheck disable=SC2154`
- Run on the CI platform shell, not just locally

## Example Response

Lists findings as `file:line:col: severity: message [SC-code]` with the explanation
link, then the agent applies the suggested fix and re-runs until clean.

## Capabilities

### shellcheck
Analyze shell scripts with severity levels, excludes, and CI formats

**Parameters:**
- `severity` (string): Minimum severity: error, warning, info, style
- `exclude` (string): Comma-separated SC codes to ignore
- `shell` (string): Shell dialect: bash, sh, dash, ksh, zsh

**Commands:**
- `shellcheck script.sh`
- `shellcheck -x scripts/*.sh`
- `shellcheck --severity=warning scripts/`
- `shellcheck --format=json script.sh > sc.json`
- `shellcheck -e SC2086,SC1091 deploy.sh`

**Examples:**
- find . -name '*.sh' -exec shellcheck {} +
- shellcheck --shell=bash --external-sources setup.sh
- shellcheck --exclude=SC2317 --format=gcc ci.sh

## References
- [ShellCheck docs](https://www.shellcheck.net/)
- [ShellCheck wiki](https://github.com/koalaman/shellcheck/wiki)
