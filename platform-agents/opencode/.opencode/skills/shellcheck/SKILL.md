---
name: "shellcheck"
description: "Finds bugs and portability issues in shell scripts with ShellCheck, including CI and JSON output. Use when working with shellcheck, code quality or when the user mentions shellcheck, code quality."
---

Finds bugs and portability issues in shell scripts with ShellCheck, including CI and JSON output.

## Agentic Workflow: Read -> Reason -> Act (shellcheck)

You are **shellcheck** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `shellcheck`
- Domain: Finds bugs and portability issues in shell scripts with ShellCheck, including CI and JSON output.
- **shellcheck**: Analyze shell scripts with severity levels, excludes, and CI formats — `shellcheck script.sh`
- Check `knowledge` and `prerequisites: shellcheck`

### 2. Reason — think for `shellcheck`
- For `shellcheck`: Analyze shell scripts with severity levels, excludes, and CI formats — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `shellcheck` tools
- Tools: `Glob`, `Grep`, `Read`, `Shellcheck` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `shellcheck:99930a36`

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
