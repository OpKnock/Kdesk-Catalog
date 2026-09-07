---
name: "postmortem"
description: "Incident postmortems: evidence gathering from logs/metrics/git, blameless writeups, and follow-up action tracking. Use when working with postmortem evidence, api or when the user mentions postmortem evidence, api."
---

Incident postmortems: evidence gathering from logs/metrics/git, blameless writeups, and follow-up action tracking.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `git log --oneline --since="2026-08-08 12:00" --until="2026-0`
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

# Postmortem

A postmortem turns an incident into durable learning: timeline, root cause, actions.

## What this skill does

- Gathers evidence: deploys, logs, events, metrics
- Drafts a blameless writeup
- Tracks follow-up actions

## When to use

- After any significant incident
- Before closing out an incident ticket

## Real commands

```bash
# Deploy timeline
 git log --oneline --since="2026-08-08 12:00" --until="2026-08-08 13:00"
 git diff --stat v2.3.0..v2.3.1

# Logs around the incident
 journalctl -u orders-api --since "2026-08-08 12:30" --until "2026-08-08 12:45" -p err

# Kubernetes evidence
 kubectl get events --sort-by=.lastTimestamp -n prod
 kubectl get pods -n prod --field-selector=status.phase=Failed
```

## Template

```markdown
# Postmortem: INC-123
## Summary
## Impact
## Timeline (UTC)
## Root cause
## Contributing factors
## Actions (owner, deadline)
## Lessons learned
```

## Best practices

- Write within 48h while memory is fresh
- Focus on systems, not people
- Every action needs an owner and due date

## Capabilities

### postmortem-evidence
Collect incident evidence from git, logs and Kubernetes events, then draft a blameless postmortem.

**Parameters:**
- `service` (string): Affected service name
- `start_time` (string): Incident start timestamp
- `window` (string): Time window for log collection

**Commands:**
- `git log --oneline --since="2026-08-08 12:00" --until="2026-08-08 13:00"`
- `journalctl -u orders-api --since "2026-08-08 12:30" --until "2026-08-08 12:45" -p err`
- `kubectl get events --sort-by=.lastTimestamp -n prod`
- `kubectl get pods -n prod -o wide --field-selector=status.phase=Failed`
- `git diff --stat v2.3.0..v2.3.1`

**Examples:**
- journalctl -u orders-api --since "2 hours ago" | grep -i "timeout"
- kubectl get events --sort-by=.lastTimestamp -n prod | grep -i crashloop
- git log --oneline v2.3.0..v2.3.1

## References
- [Google SRE Postmortem Culture](https://sre.google/sre-book/postmortem-culture.html)
- [Postmortem template (Atlassian)](https://www.atlassian.com/incident-management/postmortem/templates)
