---
type: agent_requested
description: "Runs incident response with PagerDuty CLI: declare, acknowledge, communicate, and resolve incidents with timeline notes. Use when working with pagerduty, timeline or when the user mentions pagerduty, timeline."
---

Runs incident response with PagerDuty CLI: declare, acknowledge, communicate, and resolve incidents with timeline notes.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `pd incident:list --status=triggered`, `pd note:list INCIDENT_ID`
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

# Incident Management

Respond to production incidents with a clear, auditable lifecycle.

## When to Use

- A service is down or degraded in production
- Coordinating on-call response and escalation
- Post-incident review with full timeline data

## Lifecycle

Declare -> Acknowledge -> Mitigate -> Resolve -> Review.

## Declare

```bash
pd incident:create --service-name 'Checkout' --title 'Checkout 500s' --urgency high
```

Include severity, affected scope, and the paging path in the title.

## Acknowledge and communicate

```bash
pd incident:acknowledge PXXXXX
pd note:create PXXXXX --content 'Mitigation: rolled back deploy to v2.14.3'
```

Post every material fact as a note - the timeline is the incident record.

## Resolve

```bash
pd incident:resolve PXXXXX --note 'Verified 10 min of 0% error rate; resolved by rollback'
```

## On-call context

```bash
pd schedule:oncall --time=$(date -I)
pd escalation_policy:list
```

## Post-incident review

- Timeline integrity: every mitigation step has a note.
- Classify severity and trigger conditions accurately.
- Create action items and track them as issues.
- Run blameless review: fix process, not people.

## Best practices

- Never resolve without a note describing the fix evidence.
- Keep incident titles prefixed by severity for search.
- Automate the alert route: alert -> incident creation.
- Rehearse with Game Days so the flow is muscle memory.

## Testing

Use the sandbox environment to practice the full declare-acknowledge-resolve loop.

## Capabilities

### pagerduty
Manage incidents end-to-end with the PagerDuty CLI.

**Parameters:**
- `status` (string): triggered, acknowledged, or resolved
- `service-name` (string): Service to attach the incident to
- `urgency` (string): high or low severity

**Commands:**
- `pd incident:list --status=triggered`
- `pd incident:acknowledge INCIDENT_ID`
- `pd incident:resolve INCIDENT_ID`
- `pd incident:create --service-name 'Checkout' --title 'Checkout 500s' --urgency high`
- `pd note:create INCIDENT_ID --content 'Root cause: DB replica lag; mitigation in progress'`

**Examples:**
- pd incident:list --status=triggered --status=acknowledged --format=json | jq '.incidents[].id'
- pd incident:acknowledge PXXXXX
- pd incident:resolve PXXXXX --note 'Resolved by autoscaler recovery'

### timeline
Keep an auditable incident timeline with notes and comms.

**Parameters:**
- `incident` (string): Incident id like PXXXXX
- `note` (string): Timeline note content
- `team` (string): Team name filter for incident queries

**Commands:**
- `pd note:list INCIDENT_ID`
- `pd incident:update INCIDENT_ID --status=acknowledged`
- `pd incident:list --team='Platform' --since=$(date -I) --until=$(date -I -d '+7 days')`
- `pd schedule:oncall --time=$(date -I)`
- `pd escalation_policy:list`

**Examples:**
- pd note:list PXXXXX --format=json | jq '.notes[].content'
- pd incident:update PXXXXX --status=acknowledged
- pd schedule:oncall --time=2026-08-10T14:00:00Z

## References
- [PagerDuty CLI](https://github.com/PagerDuty/pagerduty-cli)
- [PagerDuty Incident Management](https://support.pagerduty.com/docs/incidents)
- [PagerDuty API](https://developer.pagerduty.com/api-reference)