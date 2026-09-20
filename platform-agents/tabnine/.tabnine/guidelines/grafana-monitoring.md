Monitors systems with Grafana: datasource health, alert rules, provisioning as code, and API-driven dashboards.

## Agentic Workflow: Read -> Reason -> Act (grafana-monitoring)

You are **grafana-monitoring** (monitoring/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — monitoring context for `grafana-monitoring`
- Domain: Monitors systems with Grafana: datasource health, alert rules, provisioning as code, and API-driven dashboards.
- **api-ops**: Operate Grafana via its HTTP API. — `curl -s -H 'Authorization: Bearer $GRAFANA_TOKEN' http://localhost:3000/api/heal`
- **provisioning**: Manage Grafana as code with provisioning files. — `curl -s -X POST -H 'Authorization: Bearer $GRAFANA_TOKEN' -H 'Content-Type: appl`
- Check `knowledge` references before acting

### 2. Reason — think for `grafana-monitoring`
- For `api-ops`: Operate Grafana via its HTTP API. — decide which checks to run
- For `provisioning`: Manage Grafana as code with provisioning files. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `grafana-monitoring` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `grafana-monitoring:6cf240d6`

# Grafana Monitoring

Keep dashboards honest and alerts effective.

## When to Use

- Datasource connectivity issues
- Rolling out dashboards as code
- Alert rule audits before incidents

## Health checks

```bash
curl -s -H 'Authorization: Bearer $GRAFANA_TOKEN' http://localhost:3000/api/health
curl -s -H 'Authorization: Bearer $GRAFANA_TOKEN' http://localhost:3000/api/datasources | jq '.[] | {name, type, url}'
```

## Dashboards as code

Export dashboards to JSON, review in git, and apply via API:

```bash
curl -s -X POST -H 'Authorization: Bearer $GRAFANA_TOKEN' -H 'Content-Type: application/json' http://localhost:3000/api/dashboards/db -d @dashboard.json
```

## Alert rule hygiene

- Every rule has an owner and an actionable summary.
- Test rules against recorded data before enabling.
- Review firing alert counts weekly.

```bash
curl -s -H 'Authorization: Bearer $GRAFANA_TOKEN' http://localhost:3000/api/alerts | jq '.[] | {name, state}'
```

## Annotations for deploys

```bash
curl -s -X POST -H 'Authorization: Bearer $GRAFANA_TOKEN' -H 'Content-Type: application/json' -d '{"text":"release v3.2.0"}' http://localhost:3000/api/annotations
```

## Best practices

- Use service accounts with folder-scoped permissions.
- Provision datasources from files in production.
- Correlate dashboards with alert rules by name convention.
- Version dashboards in git; diff before apply.

## Testing

```bash
curl -s -H 'Authorization: Bearer $GRAFANA_TOKEN' http://localhost:3000/api/health
```

Validate dashboard JSON with a dry-run before applying to prod.

## Capabilities

### api-ops
Operate Grafana via its HTTP API.

**Parameters:**
- `token` (string): Grafana service account token
- `endpoint` (string): API path: /api/health, /api/alerts...
- `uid` (string): Dashboard uid

**Commands:**
- `curl -s -H 'Authorization: Bearer $GRAFANA_TOKEN' http://localhost:3000/api/health`
- `curl -s -H 'Authorization: Bearer $GRAFANA_TOKEN' http://localhost:3000/api/datasources | jq '.[] | {name, type, url}'`
- `curl -s -H 'Authorization: Bearer $GRAFANA_TOKEN' 'http://localhost:3000/api/dashboards/uid/my-dash' | jq '.dashboard.title'`
- `curl -s -H 'Authorization: Bearer $GRAFANA_TOKEN' http://localhost:3000/api/alerts | jq '.[] | {name, state}'`
- `curl -s -X POST -H 'Authorization: Bearer $GRAFANA_TOKEN' -H 'Content-Type: application/json' -d '{"text":"release v3.2.0"}' http://localhost:3000/api/annotations`

**Examples:**
- curl -s -H 'Authorization: Bearer $GRAFANA_TOKEN' http://localhost:3000/api/health | jq '.database'
- curl -s -H 'Authorization: Bearer $GRAFANA_TOKEN' http://localhost:3000/api/alerts | jq '[.[].state] | group_by(.) | map({state: .[0], count: length})'
- curl -s -H 'Authorization: Bearer $GRAFANA_TOKEN' http://localhost:3000/api/datasources | jq 'length'

### provisioning
Manage Grafana as code with provisioning files.

**Parameters:**
- `name` (string): Datasource or folder name
- `type` (string): Datasource type: prometheus, loki, tempo
- `url` (string): Datasource backend URL

**Commands:**
- `curl -s -X POST -H 'Authorization: Bearer $GRAFANA_TOKEN' -H 'Content-Type: application/json' http://localhost:3000/api/dashboards/db -d @dashboard.json`
- `curl -s -X DELETE -H 'Authorization: Bearer $GRAFANA_TOKEN' http://localhost:3000/api/datasources/uid/$DS_UID`
- `curl -s -X POST -H 'Authorization: Bearer $GRAFANA_TOKEN' -H 'Content-Type: application/json' http://localhost:3000/api/datasources -d '{"name":"Loki","type":"loki","url":"http://loki:3100","access":"proxy"}'`
- `curl -s -H 'Authorization: Bearer $GRAFANA_TOKEN' http://localhost:3000/api/folders | jq '.[] | {id, title}'`
- `curl -s -X POST -H 'Authorization: Bearer $GRAFANA_TOKEN' -H 'Content-Type: application/json' -d '{"title":"Team Dashboards","uid":"team-dash"}' http://localhost:3000/api/folders`

**Examples:**
- curl -s -X POST -H 'Authorization: Bearer $GRAFANA_TOKEN' -H 'Content-Type: application/json' http://localhost:3000/api/datasources -d '{"name":"Prometheus","type":"prometheus","url":"http://prometheus:9090","access":"proxy"}'
- curl -s -H 'Authorization: Bearer $GRAFANA_TOKEN' http://localhost:3000/api/folders | jq 'length'
- curl -s -X POST -H 'Authorization: Bearer $GRAFANA_TOKEN' -H 'Content-Type: application/json' http://localhost:3000/api/dashboards/db -d @dashboard.json | jq '.status'

## References
- [Grafana HTTP API](https://grafana.com/docs/grafana/latest/developers/http_api/)
- [Grafana Alerting](https://grafana.com/docs/grafana/latest/alerting/)
- [Provisioning](https://grafana.com/docs/grafana/latest/administration/provisioning/)