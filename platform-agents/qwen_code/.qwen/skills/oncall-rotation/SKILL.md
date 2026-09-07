---
name: "oncall-rotation"
description: "Queries PagerDuty on-call schedules, creates overrides for shift swaps, and lists current on-call personnel via the REST API with UTC time windows. Use when working with oncall schedule management, api or when the user mentions oncall schedule management, api."
license: "MIT"
compatibility: "Requires network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(curl:*)"
---

Queries PagerDuty on-call schedules, creates overrides for shift swaps, and lists current on-call personnel via the REST API with UTC time windows.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -H "Authorization: Token token=$PD_TOKEN" "https://api.`
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

# On-Call Rotation

Manage schedules so exactly the right person gets paged, and swap shifts cleanly with overrides.

## What this skill does

- Lists current on-call people and schedules
- Creates overrides for shift swaps
- Verifies rotation coverage over a window

## When to use

- Setting up rotations for a new team
- Checking who is on call right now
- Handling someone going on PTO

## Real commands

```bash
# Who is on call now
curl -H "Authorization: Token token=$PD_TOKEN" "https://api.pagerduty.com/oncalls"

# List schedules
curl -H "Authorization: Token token=$PD_TOKEN" "https://api.pagerduty.com/schedules"

# On-call for a window
curl -H "Authorization: Token token=$PD_TOKEN" "https://api.pagerduty.com/oncalls?since=2026-08-01&until=2026-08-31"

# Add an override
curl -X POST -H "Authorization: Token token=$PD_TOKEN" -H "Content-Type: application/json" \
  -d @override.json "https://api.pagerduty.com/schedules/SCHEDULE_ID/overrides"
```

## override.json

```json
{
  "override": {
    "start": "2026-08-15T09:00:00Z",
    "end": "2026-08-15T17:00:00Z",
    "user": { "id": "PXXXXX" }
  }
}
```

## Best practices

- Use UTC timestamps for windows and overrides
- Check coverage gaps with `escalation_policies` queries
- Rotate primary/secondary roles to avoid solo on-call

## Capabilities

### oncall-schedule-management
Query on-call schedules, add overrides, and list who is on call with the PagerDuty API.

**Parameters:**
- `token` (string): PagerDuty API token
- `schedule_id` (string): Schedule identifier
- `window` (string): since/until date range for oncalls

**Commands:**
- `curl -H "Authorization: Token token=$PD_TOKEN" "https://api.pagerduty.com/oncalls"`
- `curl -H "Authorization: Token token=$PD_TOKEN" "https://api.pagerduty.com/schedules"`
- `curl -X POST -H "Authorization: Token token=$PD_TOKEN" -H "Content-Type: application/json" -d @override.json "https://api.pagerduty.com/schedules/SCHEDULE_ID/overrides"`
- `curl -H "Authorization: Token token=$PD_TOKEN" "https://api.pagerduty.com/oncalls?since=2026-08-01&until=2026-08-31"`
- `curl -H "Authorization: Token token=$PD_TOKEN" "https://api.pagerduty.com/users"`

**Examples:**
- curl -H "Authorization: Token token=$PD_TOKEN" "https://api.pagerduty.com/oncalls?user_ids[]=PXXXXX" | jq '.oncalls[].escalation_policy.summary'
- curl -X POST -H "Authorization: Token token=$PD_TOKEN" -H "Content-Type: application/json" -d '{"override":{"start":"2026-08-15T09:00:00Z","end":"2026-08-15T17:00:00Z","user":{"id":"PXXXXX"}}}' "https://api.pagerduty.com/schedules/PSCHED/overrides"

## References
- [PagerDuty REST API](https://developer.pagerduty.com/api-reference/)
- [PagerDuty On-Call Docs](https://support.pagerduty.com/docs/schedules)
