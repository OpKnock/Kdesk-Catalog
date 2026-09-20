Automates incident response: webhook triggers, runbook dispatch via GitHub Actions, and remediation playbooks executed from alerts.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `gh workflow run runbook.yml -f severity=sev1 -f service=chec`, `curl -X POST -H 'Content-Type: application/json' -d '{"text"`
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

# Incident Response Automation

Automate the mechanical parts of incident response so humans handle judgment.

## When to Use

- Alert routing and runbook execution on page
- Automated rollback/scaling of known failure modes
- Post-incident status updates across channels

## Webhook fan-out

Alert -> webhook -> channels + ticketing + runbook:

```bash
curl -X POST -H 'Content-Type: application/json' -d '{"text":"SEV-1: checkout 500s"}' $SLACK_WEBHOOK_URL
curl -X POST -H 'Content-Type: application/json' -d '{"summary":"checkout down","priority":"high"}' $PAGERDUTY_V2_URL
```

## Runbook dispatch

```bash
gh workflow run runbook.yml -f severity=sev1 -f service=checkout
gh run watch --exit-status
```

Runbook steps: gather evidence -> stabilize (rollback/scale) -> verify -> notify.

## A minimal rollback workflow

```yaml
name: runbook
on:
  workflow_dispatch:
    inputs:
      severity: { type: choice, options: [sev1, sev2, sev3, sev4] }
      action: { type: choice, options: [rollback, scale-up, noop] }
jobs:
  mitigate:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Running ${{ github.event.inputs.action }} for ${{ github.event.inputs.severity }}"
      - run: curl -s -X POST ${{ secrets.RUNBOOK_HOOK }} -d '{"action":"${{ github.event.inputs.action }}"}'
```

## Safe automation rules

- Destructive actions always require a human approval step.
- Every automation logs its action with the incident id.
- Idempotent remediation: running twice must not double the damage.
- Keep a dead-man switch: abort automation if it exceeds a time budget.

## Testing

Dry-run the full webhook chain in staging: simulate an alert and verify channel posts, ticket creation, and runbook dispatch order.

## Capabilities

### runbook-dispatch
Trigger and monitor automated runbooks in CI pipelines.

**Parameters:**
- `severity` (string): sev1-sev4 classification
- `service` (string): Affected service name
- `action` (string): Remediation action: rollback, scale, failover

**Commands:**
- `gh workflow run runbook.yml -f severity=sev1 -f service=checkout`
- `gh run watch $(gh run list --workflow=runbook.yml --limit 1 --json databaseId -q '.[0].databaseId')`
- `gh workflow run mitigate.yml -f incident_id=P12345 -f action=rollback`
- `gh run list --workflow=runbook.yml --status=in_progress`
- `gh api repos/{owner}/{repo}/actions/runs/{run_id} | jq '.status'`

**Examples:**
- gh workflow run runbook.yml -f severity=sev1 -f service=checkout --ref main
- gh run watch --exit-status
- gh workflow run mitigate.yml -f incident_id=P12345

### webhooks
Wire alerts to chat and ticketing systems via webhooks.

**Parameters:**
- `webhook-url` (string): Slack/PD/ticketing webhook endpoint
- `payload` (string): JSON alert payload
- `incident-id` (string): Incident identifier for correlation

**Commands:**
- `curl -X POST -H 'Content-Type: application/json' -d '{"text":"SEV-1: checkout 500s"}' $SLACK_WEBHOOK_URL`
- `curl -X POST -H 'Content-Type: application/json' -d '{"summary":"checkout down","priority":"high"}' $PAGERDUTY_V2_URL`
- `curl -X POST -H 'Content-Type: application/json' -H 'Authorization: Bearer $LINEAR_TOKEN' -d '{"teamId":"...","title":"SEV-1 checkout"}' https://api.linear.app/graphql`
- `curl -s -X POST $WEBHOOK_RECEIVER -d '{"event":"incident.created","id":"P12345"}'`
- `curl -i -X POST -H 'Content-Type: application/json' -d '{"incident":"P12345","status":"mitigated"}' $RUNBOOK_HOOK`

**Examples:**
- curl -X POST -H 'Content-Type: application/json' -d '{"text":"Rollback complete for P12345"}' $SLACK_WEBHOOK_URL
- curl -X POST -d '{}' $PAGERDUTY_V2_URL
- curl -s -X POST $RUNBOOK_HOOK -d '{"severity":"sev2"}'

## References
- [GitHub Actions](https://docs.github.com/en/actions)
- [Slack incoming webhooks](https://api.slack.com/messaging/webhooks)
- [PagerDuty Events API v2](https://developer.pagerduty.com/docs/events-api-v2/)