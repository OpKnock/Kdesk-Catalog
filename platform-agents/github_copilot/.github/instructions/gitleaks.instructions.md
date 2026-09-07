---
applyTo: "**/*.go **/*.json **/*.r **/*.sh"
---

Detects hardcoded secrets in git history and files with gitleaks, including CI-safe configs and custom allowlists.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `gitleaks detect --source . -v`, `gitleaks generate`
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

# gitleaks

Secret scanning for git repositories with SAST-grade accuracy.

## What This Skill Does

- Scans commits, branches, tags, and the working tree for 100+ secret types
- Runs as a pre-commit hook and in CI
- Generates custom rule configs with allowlists
- Produces JSON/SARIF reports for triage

## When to Use

- Auditing a repo before making it public
- Enforcing no-new-secrets policy in CI
- Discovering how far back a leaked key goes

## Real Commands

```bash
# Basic working tree scan
 gitleaks detect --source . -v

# Full history scan
gitleaks git --log-opts="--all"

# Remote repo scan
gitleaks git --remote https://github.com/org/repo

# Protect staged changes before commit
gitleaks protect --staged

# Generate a config to customize
 gitleaks generate > gitleaks.toml
 gitleaks detect --source . --config gitleaks.toml --report-path report.json
```

## Sample Config (allowlist)

```toml
[extend]
useDefault = true

[[rules]]
id = "custom-aws-access-key"
description = "AWS access key"
regex = '''AKIA[0-9A-Z]{16}'''

[[rules.allowlists]]
description = "test fixtures"
regexes = ['''AKIA0000000000000000''']
paths = ['''fixtures/.*''']
```

## Best Practices

- Scan full history once, then gate on new commits in CI
- Use --redact in logs so secrets never hit your terminal/CI logs
- Rotate any secret found in history; purging history is not enough
- Keep an allowlist for fixtures, but review it in PRs
- Export findings to SARIF for GitHub code scanning annotations

## Capabilities

### secret-detection
Scan working trees, git history, and stashes for leaked secrets.

**Parameters:**
- `source` (string): Directory or repo to scan
- `logOpts` (string): Git log options to limit scan range
- `redact` (boolean): Mask secret values in output

**Commands:**
- `gitleaks detect --source . -v`
- `gitleaks git --log-opts="--all"`
- `gitleaks git --remote https://github.com/org/repo`
- `gitleaks detect --source . --redact`
- `gitleaks detect --source . --exit-code 1`

**Examples:**
- gitleaks detect --source . -v
- gitleaks git --log-opts="--all"
- gitleaks detect --source . --redact

### config-and-ci
Generate baseline configs and run gitleaks in CI workflows.

**Parameters:**
- `config` (string): Custom config TOML path
- `reportPath` (string): Output report file path

**Commands:**
- `gitleaks generate`
- `gitleaks detect --source . --config gitleaks.toml`
- `gitleaks protect --staged`
- `gitleaks secret-key`
- `gitleaks detect --source . --report-path report.json --report-format json`

**Examples:**
- gitleaks generate > gitleaks.toml
- gitleaks protect --staged
- gitleaks detect --source . --report-path gitleaks-report.json

## References
- [gitleaks GitHub](https://github.com/gitleaks/gitleaks)
- [gitleaks Configuration](https://github.com/gitleaks/gitleaks#configuration)
