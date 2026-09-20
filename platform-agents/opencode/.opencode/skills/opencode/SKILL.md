---
name: "opencode"
description: "Operates the opencode CLI agent: run tasks headlessly, manage auth and providers, configure models, and manage sessions. Use when working with agent runs, auth and config, devtools or when the user mentions agent runs, auth and config, devtools."
---

Operates the opencode CLI agent: run tasks headlessly, manage auth and providers, configure models, and manage sessions.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `opencode`, `opencode auth login`
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

# opencode CLI Agent

Drive the opencode AI coding agent from the terminal.

## What This Skill Does

- Starts interactive agent sessions
- Runs headless task prompts with specific models
- Manages provider authentication
- Serves opencode over HTTP for integrations
- Tunes output with flags and output modes

## When to Use

- Automating code tasks from scripts/CI
- Delegating repo-wide refactors to an agent
- Choosing models per task difficulty

## Real Commands

```bash
# Interactive
opencode
opencode --model claude-sonnet-4

# Headless task runs
opencode run 'fix the failing test in src/'
opencode run --model gpt-5 'explain the auth flow in this repo'
opencode run -o output.txt 'generate a migration plan'
opencode run --continue 'now apply the plan'

# Auth and providers
opencode auth login
opencode auth logout
opencode auth list

# Server mode
opencode serve

# Diagnostics
opencode --print-logs
opencode --help
```

## Best Practices

- Start with --print-logs when debugging agent behavior
- Use --continue to chain follow-up tasks on one session
- Pin --model per task type (cheap model for summaries)
- Use headless mode with output files for CI automation
- Keep the agent focused: one clear goal per prompt

## Capabilities

### agent-runs
Run opencode agents in the terminal and headlessly.

**Parameters:**
- `prompt` (string): Task prompt
- `model` (string): Model provider:model id

**Commands:**
- `opencode`
- `opencode run 'fix the failing test in src/'`
- `opencode run --model claude-sonnet-4 'explain this repo'`
- `opencode run -o share.json 'summarize changes'`
- `opencode --print-logs`

**Examples:**
- opencode run 'fix the failing test in src/'
- opencode run --model claude-sonnet-4 'explain this repo'
- opencode --print-logs

### auth-and-config
Authenticate providers and manage opencode configuration.

**Parameters:**
- `provider` (string): Auth provider
- `scope` (string): Auth scope requested at login

**Commands:**
- `opencode auth login`
- `opencode auth logout`
- `opencode auth list`
- `opencode serve`
- `opencode --help`

**Examples:**
- opencode auth login
- opencode auth list
- opencode serve

## References
- [opencode Documentation](https://opencode.ai/docs)
- [opencode GitHub](https://github.com/anomalyco/opencode)
