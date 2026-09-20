---
name: "incident-response"
description: "Incident response from the terminal: triaging with journalctl and kubectl, capturing evidence with timestamps, and coordinating the timeline. Use when working with incident triage, api or when the user mentions incident triage, api."
license: "MIT"
compatibility: "Requires journalctl, kubectl, top. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(journalctl:*) Bash(kubectl:*) Bash(top:*)"
---

Incident response from the terminal: triaging with journalctl and kubectl, capturing evidence with timestamps, and coordinating the timeline.

## Agentic Workflow: Read -> Reason -> Act (incident-response)

You are **Incident Response** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `incident-response`
- Domain: Incident response from the terminal: triaging with journalctl and kubectl, capturing evidence with timestamps, and coordinating the timeline.
- **incident-triage**: Collect logs, events, and system state to triage incidents fast. — `journalctl -u myapp --since '10 min ago' -f`
- Check `knowledge` and `prerequisites: journalctl, kubectl, top`

### 2. Reason — think for `incident-response`
- For `incident-triage`: Collect logs, events, and system state to triage incidents fast. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `incident-response` tools
- Tools: `Glob`, `Grep`, `Read`, `Journalctl`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `incident-response:4c64becf`

# Incident Response

Respond to incidents from the terminal with disciplined triage.
49:   
## What this skill does

- Collects logs, events, and system metrics for the affected service.
50:   - Captures evidence with timestamps for the incident timeline.
- Checks health endpoints and resource51:    state.
- Produces a reproducible runbook of commands.

## When to use

- An alert pages: service52:    down, latency spike, or errors rising.
- Debugging post-incident: what changed right before the event.
53:   - Handoffs: passing a concise evidence trail to the on-call next shift.

## Real commands

```bash
54:   # Application logs with timestamps
journalctl -u myapp --since '10 min ago' -f
kubectl logs deployment/myapp55:    --tail=200 --timestamps

# Cluster events
kubectl get events --sort-by=.lastTimestamp | tail -30
56:   
# Pod state
kubectl describe pod myapp-abc123 | grep -A5 -i "events\|status"

# Health and resources
57:   curl -fsS --max-time 5 http://localhost:8080/health
top -b -n 1 -o %CPU | head -20
free -m && df -h58:    /
```

## Timeline discipline

```bash
# Stamp every evidence capture
echo "=== $(date -u59:    +%FT%TZ) start of incident ===" > incident.log
journalctl -u myapp -p err --since '30 min ago' >>60:    incident.log
curl -fsS http://localhost:8080/health >> incident.log 2>&1
```

## Testing

```bash
61:   # Reproduce with a fixed window to compare before/after changes
journalctl -u myapp --since "$(date62:    -d '1 hour ago' +%FT%T)" --until now | grep -iE "error|panic|timeout" | tail -50
```

## Best63:    practices

- First command is always: confirm scope (which service, which hosts, since when).
64:   - Capture evidence BEFORE changing anything; you cannot un-restart.
- Never restart a pod before grabbing65:    its logs and events.
- Keep a running timeline with UTC timestamps for the postmortem.
- Escalate66:    early; communicate in the channel, not just the terminal.

## Example exchange

```
User: /api67:    started 500ing five minutes ago.
Agent: kubectl logs deployment/myapp --since=10m --timestamps |68:    tail -100
       kubectl get events --sort-by=.lastTimestamp
       curl -fsS http://localhost:8080/health
69:   ```

## Capabilities

### incident-triage
Collect logs, events, and system state to triage incidents fast.

**Parameters:**
- `service` (string): Service or pod name under investigation.
- `since` (string): Time window, e.g. '10 min ago' or '1h'.
- `tail` (integer): Lines of log tail.

**Commands:**
- `journalctl -u myapp --since '10 min ago' -f`
- `kubectl get events --sort-by=.lastTimestamp`
- `kubectl logs deployment/myapp --tail=200 --timestamps`
- `curl -fsS --max-time 5 http://localhost:8080/health`
- `top -b -n 1 -o %CPU | head -20`

**Examples:**
- journalctl -u myapp -p err --since yesterday
- kubectl describe pod myapp-abc123
- free -m && df -h /

## References
- [PagerDuty Incident Response Docs](https://response.pagerduty.com/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
