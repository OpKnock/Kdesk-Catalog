---
name: "postmortem"
description: "Incident postmortems: evidence gathering from logs/metrics/git, blameless writeups, and follow-up action tracking."
---

# Postmortem

Incident postmortems: evidence gathering from logs/metrics/git, blameless writeups, and follow-up action tracking.

## Instructions

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
