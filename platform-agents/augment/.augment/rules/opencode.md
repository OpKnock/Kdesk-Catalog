---
type: agent_requested
description: "Operates the opencode CLI agent: run tasks headlessly, manage auth and providers, configure models, and manage sessions."
---

# Opencode

Operates the opencode CLI agent: run tasks headlessly, manage auth and providers, configure models, and manage sessions.

## Instructions

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