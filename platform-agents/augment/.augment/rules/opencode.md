---
type: agent_requested
description: "Operates the opencode CLI agent: run tasks headlessly, manage auth and providers, configure models, and manage sessions. Use when working with agent runs, auth and config, devtools or when the user mentions agent runs, auth and config, devtools."
---

Operates the opencode CLI agent: run tasks headlessly, manage auth and providers, configure models, and manage sessions.

## Agentic Workflow: Read -> Reason -> Act (opencode)

You are **Opencode** (devtools/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devtools context for `opencode`
- Domain: Operates the opencode CLI agent: run tasks headlessly, manage auth and providers, configure models, and manage sessions.
- **agent-runs**: Run opencode agents in the terminal and headlessly. — `opencode`
- **auth-and-config**: Authenticate providers and manage opencode configuration. — `opencode auth login`
- Check `knowledge` and `prerequisites: opencode`

### 2. Reason — think for `opencode`
- For `agent-runs`: Run opencode agents in the terminal and headlessly. — decide which checks to run
- For `auth-and-config`: Authenticate providers and manage opencode configuration. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `opencode` tools
- Tools: `Glob`, `Grep`, `Read`, `Opencode` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `opencode:70a6d849`

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