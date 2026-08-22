---
name: "Grafana Dashboards"
description: "Grafana dashboard management: provision dashboards via API and files, create panels and alerts, and query data sources from the CLI."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
alwaysApply: false
---

# Grafana Dashboards

Grafana dashboard management: provision dashboards via API and files, create panels and alerts, and query data sources from the CLI.

## Instructions

# Grafana Dashboards

## What this skill does

Grafana visualizes metrics and logs in dashboards. This skill covers dashboard lifecycle through the API: search, export, create, and delete, plus panel query inspection.

## When to use

- Rolling out dashboards as code
- Inspecting what a panel actually queries
- Migrating dashboards between Grafana instances

## Real commands

```bash
# Search dashboards
curl -s -H 'Authorization: Bearer $GRAFANA_TOKEN' http://localhost:3000/api/search?type=dash-db | jq '.[] | {uid, title}'

# Export and inspect panels
curl -s -H 'Authorization: Bearer $GRAFANA_TOKEN' http://localhost:3000/api/dashboards/uid/orders-overview | jq '.dashboard.panels[0].targets[0].expr'

# Import a dashboard JSON
curl -s -X POST -H 'Authorization: Bearer $GRAFANA_TOKEN' -H 'Content-Type: application/json' http://localhost:3000/api/dashboards/db -d @dashboard.json | jq '.status'

# Delete
curl -s -X DELETE -H 'Authorization: Bearer $GRAFANA_TOKEN' http://localhost:3000/api/dashboards/uid/orders-overview | jq '.title'

# Plugins
 grafana-cli plugins list
```

## Dashboard JSON shape

```json
{
  "dashboard": {
    "title": "Orders Overview",
    "uid": "orders-overview",
    "panels": [
      {
        "title": "Request rate",
        "type": "timeseries",
        "targets": [{"expr": "sum(rate(http_requests_total{job=\"orders\"}[5m]))", "refId": "A"}]
      }
    ],
    "time": {"from": "now-1h", "to": "now"}
  },
  "overwrite": true
}
```

## Testing

```bash
# After import, verify the panel resolves
curl -s -H 'Authorization: Bearer $GRAFANA_TOKEN' 'http://localhost:3000/api/ds/query' -H 'Content-Type: application/json' -d '{"queries":[{"expr":"up","refId":"A"}],"from":"now-5m","to":"now"}' | jq '.results.A.frames[0].data' | head -5
```

## Best practices

- Manage dashboards as JSON in git; import via API or provisioning files.
- Keep panel queries readable; add refIds and comments.
- Use template variables for environment/instance filtering.
- Set versioned UIDs so imports overwrite cleanly.
- Enable annotations from data sources to correlate with deploys.

## Capabilities

### grafana-provisioning
Provision, export, and manage dashboards via the Grafana HTTP API.

**Commands:**
- `grafana-cli plugins list`
- `curl -s -H 'Authorization: Bearer $GRAFANA_TOKEN' http://localhost:3000/api/search?type=dash-db | jq '.[] | {uid, title}'`
- `curl -s -H 'Authorization: Bearer $GRAFANA_TOKEN' http://localhost:3000/api/dashboards/uid/orders-overview | jq '.dashboard.title'`
- `curl -s -X POST -H 'Authorization: Bearer $GRAFANA_TOKEN' -H 'Content-Type: application/json' http://localhost:3000/api/dashboards/db -d @dashboard.json | jq '.status'`
- `curl -s -H 'Authorization: Bearer $GRAFANA_TOKEN' 'http://localhost:3000/api/dashboards/uid/orders-overview' | jq '.dashboard.panels[0].targets[0].expr'`
- `curl -s -X DELETE -H 'Authorization: Bearer $GRAFANA_TOKEN' http://localhost:3000/api/dashboards/uid/orders-overview | jq '.title'`

**Examples:**
- curl -s -H 'Authorization: Bearer $GRAFANA_TOKEN' http://localhost:3000/api/search?type=dash-db | jq '.[] | {uid, title}'
- curl -s -X POST -H 'Authorization: Bearer $GRAFANA_TOKEN' -H 'Content-Type: application/json' http://localhost:3000/api/dashboards/db -d @dashboard.json | jq '.status'
- curl -s -H 'Authorization: Bearer $GRAFANA_TOKEN' http://localhost:3000/api/dashboards/uid/orders-overview | jq '.dashboard.panels[0].targets[0].expr'