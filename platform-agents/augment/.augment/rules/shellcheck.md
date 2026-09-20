---
type: agent_requested
description: "Finds bugs and portability issues in shell scripts with ShellCheck, including CI and JSON output."
---

# shellcheck

Finds bugs and portability issues in shell scripts with ShellCheck, including CI and JSON output.

## Instructions

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