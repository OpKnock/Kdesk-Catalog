---
applyTo: "**/*.r **/*.sh"
---

Writes robust POSIX/bash scripts: syntax checking, shellcheck linting, error handling with set -euo pipefail, and cross-platform portability.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `bash -n script.sh`, `set -euo pipefail`
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

# Shell Scripting

Write correct, portable, debuggable shell scripts.

## What This Skill Does

- Checks syntax and lints with shellcheck
- Formats consistently with shfmt
- Enforces strict error handling (set -euo pipefail)
- Uses traps for cleanup and error reporting
- Handles args, env vars, and external tool checks

## When to Use

- Automating CI steps, deploys, or ops tasks
- Porting scripts between bash/sh environments
- Debugging subtle quoting and expansion bugs

## Real Commands

```bash
# Validate
bash -n script.sh
shellcheck script.sh
shellcheck -x -S warning script.sh    # follow sources, min severity
shfmt -w script.sh
checkbashisms script.sh               # POSIX portability

# Debug
bash -x script.sh
bash -x -v script.sh

# Strict patterns
set -euo pipefail
trap 'echo failed at line $LINENO' ERR
command -v jq >/dev/null || { echo 'jq is required'; exit 1; }
readonly CONFIG=/etc/app.conf
local TMPFILE=$(mktemp)
trap 'rm -f "$TMPFILE"' EXIT
```

## Script Skeleton

```bash
#!/usr/bin/env bash
set -euo pipefail

usage() { echo "usage: $0 <env>"; exit 1; }
[[ $# -eq 1 ]] || usage

env="$1"
echo "deploying to $env"
```

## Best Practices

- Always lint with shellcheck before committing
- Quote every expansion: "$var", "$(cmd)"
- Use -euo pipefail in every non-interactive script
- Use local in functions; mktemp + EXIT trap for temp files
- Prefer bash -n in CI pre-commit hooks

## Capabilities

### script-quality
Validate and lint shell scripts for correctness.

**Parameters:**
- `script` (string): Script file path
- `severity` (string): Minimum severity: error, warning, info, style

**Commands:**
- `bash -n script.sh`
- `shellcheck script.sh`
- `shellcheck -x -S warning script.sh`
- `shfmt -w script.sh`
- `bash -x script.sh`
- `checkbashisms script.sh`

**Examples:**
- bash -n script.sh
- shellcheck -x -S warning script.sh
- shfmt -w script.sh

### robust-patterns
Write error-safe scripts with strict mode and defensive patterns.

**Parameters:**
- `var` (string): Variable name for readonly/local
- `timeout-seconds` (integer): Timeout for guarded commands

**Commands:**
- `set -euo pipefail`
- `trap 'echo failed at line $LINENO; exit 1' ERR`
- `timeout 60 curl -sS http://localhost:8080`
- `command -v jq >/dev/null || { echo 'jq required'; exit 1; }`
- `readonly CONFIG=/etc/app.conf`
- `local TMPFILE=$(mktemp)`

**Examples:**
- set -euo pipefail
- trap 'echo failed at line $LINENO' ERR
- command -v jq >/dev/null || exit 1

## References
- [ShellCheck](https://www.shellcheck.net/)
- [Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html)
- [POSIX Shell Utilities](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/contents.html)
