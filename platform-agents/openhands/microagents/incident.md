---
name: "incident"
description: "Coordinates incident response with PagerDuty, incident.io, and status pages, managing acknowledgements, escalations, and postmortems."
type: knowledge
triggers: ["incident", "pagerduty-management", "incidentio-declarations", "status-pages"]
---

# Incident

Coordinates incident response with PagerDuty, incident.io, and status pages, managing acknowledgements, escalations, and postmortems.

## Instructions

# Incident Response

Own the incident lifecycle: detect, acknowledge, mitigate, communicate, and learn.

## What This Skill Does

- Triages incidents from PagerDuty and incident.io
- Moves incidents through acknowledge/mitigate/resolve states
- Posts status page updates for external communication
- Captures notes and timelines for postmortems

## When to Use

- An alert page triggers and needs triage
- Coordinating on-call response
- Publishing communication during a major outage

## Real Commands

```bash
# PagerDuty
pd incident list --status trigger
pd incident show INCIDENT_ID
pd incident update INCIDENT_ID --status acknowledged
pd incident update INCIDENT_ID --status resolved

# incident.io
incidentio incident declare --summary 'API latency spike' --severity critical
incidentio incident list --status open
incidentio incident note add INCIDENT_ID --text 'Rolled back v1.2.3'

# Statuspage
curl -s -X POST https://api.statuspage.io/v1/pages/PAGE_ID/incidents \
  -d '{"incident":{"name":"Degraded API","status":"investigating"}}' \
  -H "Authorization: OAuth $KEY" | jq .
```

## Response Playbook

1. Acknowledge the alert immediately (pd incident update --status acknowledged)
2. Declare severity and assemble responders
3. Mitigate first (rollback, scale, isolate), investigate second
4. Update status page every 30 minutes during active incidents
5. Resolve only after monitoring confirms stability
6. Schedule the postmortem within 48 hours

## Best Practices

- Acknowledge fast; automate acks for known noise
- Keep communication in one thread (incident channel + notes)
- Never resolve while symptoms persist
- Track action items from postmortems to completion
- Rehearse runbooks during low-severity incidents

## Capabilities

### pagerduty-management
List, acknowledge, and resolve PagerDuty incidents.

**Commands:**
- `pd incident list --status trigger`
- `pd incident show INCIDENT_ID`
- `pd incident update INCIDENT_ID --status acknowledged`
- `pd incident update INCIDENT_ID --status resolved`
- `pd team list`

**Examples:**
- pd incident list --status trigger
- pd incident update INCIDENT_ID --status acknowledged
- pd incident update INCIDENT_ID --status resolved

### incidentio-declarations
Declare and manage incidents with incident.io CLI.

**Commands:**
- `incidentio incident declare --summary 'API latency spike' --severity critical`
- `incidentio incident list --status open`
- `incidentio incident update INCIDENT_ID --status mitigating`
- `incidentio incident note add INCIDENT_ID --text 'Rolled back v1.2.3'`
- `incidentio incident list --severity major`

**Examples:**
- incidentio incident declare --summary 'DB CPU at 100%' --severity major
- incidentio incident update INCIDENT_ID --status resolved
- incidentio incident note add INCIDENT_ID --text 'Root cause identified'

### status-pages
Post status updates and component maintenance.

**Commands:**
- `curl -s -X POST https://api.statuspage.io/v1/pages/PAGE_ID/incidents -d '{"incident":{"name":"...","status":"investigating"}}' -H "Authorization: OAuth $KEY"`
- `curl -s https://api.statuspage.io/v1/pages/PAGE_ID/incidents -H "Authorization: OAuth $KEY" | jq .`
- `curl -s -X POST https://api.statuspage.io/v1/pages/PAGE_ID/components -d '{"component":{"name":"API"}}' -H "Authorization: OAuth $KEY" | jq .`

**Examples:**
- curl -s https://api.statuspage.io/v1/pages/PAGE_ID/incidents -H "Authorization: OAuth $KEY" | jq .
- curl -s -X PATCH https://api.statuspage.io/v1/pages/PAGE_ID/incidents/ID -d '{"incident":{"status":"monitoring"}}' -H "Authorization: OAuth $KEY" | jq .
