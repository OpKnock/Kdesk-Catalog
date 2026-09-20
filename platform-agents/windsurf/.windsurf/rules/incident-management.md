---
trigger: glob
description: "Runs incident response with PagerDuty CLI: declare, acknowledge, communicate, and resolve incidents with timeline notes. Use when working with pagerduty, timeline or when the user mentions pagerduty, timeline."
globs: ["**/*.r", "**/*.scala", "**/*.sh"]
---

Runs incident response with PagerDuty CLI: declare, acknowledge, communicate, and resolve incidents with timeline notes.

## Agentic Workflow: Read -> Reason -> Act (incident-management)

You are **incident-management** (sre) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — sre context for `incident-management`
- Domain: Runs incident response with PagerDuty CLI: declare, acknowledge, communicate, and resolve incidents with timeline notes.
- **pagerduty**: Manage incidents end-to-end with the PagerDuty CLI. — `pd incident:list --status=triggered`
- **timeline**: Keep an auditable incident timeline with notes and comms. — `pd note:list INCIDENT_ID`
- Check `knowledge` and `prerequisites: pagerduty, opsgenie, slack, jira`

### 2. Reason — think for `incident-management`
- For `pagerduty`: Manage incidents end-to-end with the PagerDuty CLI. — decide which checks to run
- For `timeline`: Keep an auditable incident timeline with notes and comms. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `incident-management` tools
- Tools: `Glob`, `Grep`, `Read`, `Pd` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `incident-management:82719651`

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
