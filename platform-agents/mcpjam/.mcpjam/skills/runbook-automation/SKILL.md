---
name: "runbook-automation"
description: "Expert reference for automating incident runbooks end to end with kubectl/journalctl checks, Slack webhook alerts, PagerDuty event API, and scripted remediation playbooks. Use when working with incident runbook, api or when the user mentions incident runbook, api."
license: "MIT"
compatibility: "Requires ansible-playbook, journalctl, kubectl. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(ansible-playbook:*) Bash(curl:*) Bash(journalctl:*) Bash(kubectl:*)"
---

Expert reference for automating incident runbooks end to end with kubectl/journalctl checks, Slack webhook alerts, PagerDuty event API, and scripted remediation playbooks.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `kubectl describe pod api-7d9f -n prod | tail -40`
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

# Runbook Automation

Expert skill for automating incident runbooks end to end.

## What this skill does

- Gathers diagnostics fast: pod state, logs, recent events
- Pages humans with Slack webhooks and PagerDuty events
- Runs scripted remediation with Ansible or shell

## When to use

- On-call pages for symptoms that have known fixes
- Standardizing what the first responder actually runs
- Wiring probes to paging instead of manual checks

## Real commands

```bash
# Diagnose
kubectl describe pod api-7d9f -n prod | tail -40
kubectl get events -n prod --sort-by=.lastTimestamp | tail -20
journalctl -u api -n 100 --no-pager

# Alert to Slack
curl -X POST https://hooks.slack.com/services/T123456/B789012/XYZ789 -H 'Content-Type: application/json' -d '{"text":":fire: API latency above 5s"}'

# Page via PagerDuty Events API v2
curl -X POST -H 'Content-Type: application/json' -H 'X-Routing-Key: rk_abc123def456' -d '{"event_type":"trigger","payload":{"summary":"API down","source":"probe"}}' https://events.pagerduty.com/v2/enqueue

# Remediate
ansible-playbook -i inventory.ini runbooks/restart-api.yml
```

## Playbook skeleton

```yaml
- hosts: api
  tasks:
    - name: Restart api service
      ansible.builtin.service:
        name: api
        state: restarted
```

## Testing

```bash
# Dry-run remediation
ansible-playbook -i inventory.ini runbooks/restart-api.yml --check
# Test the webhook with a benign message
curl -X POST https://hooks.slack.com/services/T123456/B789012/XYZ789 -H 'Content-Type: application/json' -d '{"text":"test"}'
```

## Best practices

- Every runbook step must be a single command or script
- Test webhooks before incidents; use pagerduty resolve on recovery
- Log which runbook fired and its outcome to your ops store

## Capabilities

### incident-runbook
Automate incident response: diagnose, alert, remediate

**Parameters:**
- `webhook_url` (string): Slack incoming webhook URL
- `service` (string): systemd unit or k8s service name
- `playbook` (string): Ansible playbook path

**Commands:**
- `kubectl describe pod api-7d9f -n prod | tail -40`
- `journalctl -u api -n 100 --no-pager`
- `curl -X POST https://hooks.slack.com/services/T123456/B789012/XYZ789 -H 'Content-Type: application/json' -d '{"text":":fire: API latency above 5s"}'`
- `curl -X POST -H 'Content-Type: application/json' -H 'X-Routing-Key: rk_abc123def456' -d '{"event_type":"trigger","payload":{"summary":"API down","source":"probe"}}' https://events.pagerduty.com/v2/enqueue`
- `ansible-playbook -i inventory.ini runbooks/restart-api.yml`

**Examples:**
- journalctl -u api -n 100 --no-pager -f
- curl -X POST https://hooks.slack.com/services/T123456/B789012/XYZ789 -H 'Content-Type: application/json' -d '{"text":"deploy finished"}'
- kubectl get events -n prod --sort-by=.lastTimestamp | tail -20

## References
- [Slack incoming webhooks](https://api.slack.com/messaging/webhooks)
- [PagerDuty Events API v2](https://developer.pagerduty.com/docs/events-api-v2/trigger-events/)
