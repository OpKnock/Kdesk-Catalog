---
name: "shell-scripting"
description: "Writes robust POSIX/bash scripts: syntax checking, shellcheck linting, error handling with set -euo pipefail, and cross-platform portability."
---

# shell-scripting

Writes robust POSIX/bash scripts: syntax checking, shellcheck linting, error handling with set -euo pipefail, and cross-platform portability.

## Instructions

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
