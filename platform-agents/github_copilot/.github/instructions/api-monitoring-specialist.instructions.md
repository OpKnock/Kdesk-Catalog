---
applyTo: "**/*.json **/*.r **/*.sh **/*.{yaml,yml}"
---

Configures alerting and SLOs for API services: Prometheus alert rules, Alertmanager routes and silence management with amtool, and SLO burn-rate alerts.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -s -X POST http://localhost:9093/api/v2/alerts -H 'Cont`, `promtool check rules slo-rules.yml`
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

# API Monitoring Specialist

Alerting and SLO engineering for APIs.

## What This Skill Does
- Defines burn-rate alert rules for error and latency SLOs
- Routes alerts to teams with Alertmanager
- Manages silences during maintenance windows

## When to Use
- Setting up paging for API error budgets
- Reducing alert noise with proper routing
- Auditing who silenced what and when

## Real Commands

```bash
amtool check config alertmanager.yml
curl -s http://localhost:9093/api/v2/status | jq '.version'
amtool alert add 30m 'APIHighErrorRate' 'service=api'
```

## Burn-Rate Alert

```yaml
groups:
  - name: api-slo
    rules:
      - alert: APIErrorBudgetBurn
        expr: (1 - sum(rate(http_requests_total{code=~"5.."}[30m])) / sum(rate(http_requests_total[30m]))) < 0.95
        for: 15m
        labels: { severity: page }
```

## Testing
- Validate rule syntax with promtool check rules
- Use promtool test rules with fixture data
- Verify silence matches with amtool silence query

## Best Practices
- Alert on burn rate, not raw error count
- Route by severity and team labels
- Review silence expiry in on-call rotations

## Capabilities

### alertmanager
Operate Alertmanager and manage silences

**Parameters:**
- `config-file` (string): alertmanager.yml path
- `matchers` (array): Label matchers for silences and routing
- `duration` (string): Silence duration like 30m or 4h

**Commands:**
- `curl -s -X POST http://localhost:9093/api/v2/alerts -H 'Content-Type: application/json' -d '[{"labels":{"alertname":"APIHighErrorRate","service":"api"},"annotations":{"summary":"Error rate above 5%"}}]'`
- `curl -s http://localhost:9093/api/v2/status | jq '.version'`
- `amtool alert add 30m 'APIHighErrorRate' 'service=api' --annotation=summary='Errors high'`
- `amtool check config alertmanager.yml`
- `curl -s -X POST http://localhost:9093/api/v2/silences -H 'Content-Type: application/json' -d '{"matchers":[{"name":"service","value":"api"}],"startsAt":"2024-01-01T00:00:00Z","endsAt":"2024-01-02T00:00:00Z","createdBy":"ops","comment":"planned deploy"}'`

**Examples:**
- amtool check config validates alertmanager.yml syntax
- POST /api/v2/silences suppresses alerts during maintenance
- curl localhost:9093/api/v2/alerts lists active alert instances

### slo-rules
Define and test SLO burn-rate alert rules

**Commands:**
- `promtool check rules slo-rules.yml`
- `promtool test rules slo-tests.yml`
- `curl -s 'http://localhost:9090/api/v1/rules?type=alert' | jq '.data.groups | length'`

**Examples:**
- -cli --help
- -api --help

## References
- [Alertmanager Docs](https://prometheus.io/docs/alerting/latest/alertmanager/)
- [amtool Docs](https://prometheus.io/docs/alerting/latest/amtool/)
