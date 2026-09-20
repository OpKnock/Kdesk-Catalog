---
name: "grafana"
description: "Operates Grafana: plugin management, admin tasks, dashboard provisioning, and API-driven configuration."
type: knowledge
triggers: ["grafana", "grafana-cli", "api"]
---

# grafana

Operates Grafana: plugin management, admin tasks, dashboard provisioning, and API-driven configuration.

## Instructions

# Grafana

Run Grafana reliably: plugins, admin recovery, and automation.

## When to Use

- Installing and updating Grafana plugins
- Recovering admin access
- Managing dashboards and datasources programmatically

## Plugin management

```bash
grafana-cli plugins install grafana-clock-panel
grafana-cli plugins update-all
grafana-cli plugins list
```

## Admin recovery

```bash
grafana-cli --homepath /usr/share/grafana admin reset-admin-password 'new-secret-pass'
```

Reset passwords only via the CLI on the server; never share the admin account.

## Provisioning (recommended)

```yaml
# /etc/grafana/provisioning/datasources/prometheus.yaml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
```

Dashboards and datasources in provisioning folders are versioned and reloaded automatically.

## API automation

```bash
curl -s -H 'Authorization: Bearer $GRAFANA_API_KEY' http://localhost:3000/api/datasources
curl -s -X POST -H 'Authorization: Bearer $GRAFANA_API_KEY' -H 'Content-Type: application/json' http://localhost:3000/api/dashboards/db -d @dashboard.json
```

Create service accounts with scoped tokens instead of admin API keys.

## Annotations for deploys

```bash
curl -s -X POST -H 'Authorization: Bearer $KEY' -H 'Content-Type: application/json' -d '{"text":"deploy v2.14.3"}' http://localhost:3000/api/annotations
```

## Best practices

- Provision everything as code; manual UI changes drift.
- Keep plugin versions pinned in the image.
- Alert on datasource health via blackbox probes.

## Testing

```bash
curl -s -H 'Authorization: Bearer $KEY' http://localhost:3000/api/search?type=dash-db | jq length
```

Verify dashboards count after provisioning.

## Capabilities

### grafana-cli
Manage plugins and admin access from the command line.

**Commands:**
- `grafana-cli plugins install grafana-clock-panel`
- `grafana-cli plugins update-all`
- `grafana-cli plugins list`
- `grafana-cli admin reset-admin-password new-secret-pass`
- `grafana-cli --homepath /usr/share/grafana admin reset-admin-password`

**Examples:**
- grafana-cli plugins install grafana-piechart-panel --pluginsDir /var/lib/grafana/plugins
- grafana-cli plugins list --config /etc/grafana/grafana.ini
- grafana-cli admin reset-admin-password admin

### api
Drive Grafana configuration via the HTTP API.

**Commands:**
- `curl -s -H 'Authorization: Bearer $GRAFANA_API_KEY' http://localhost:3000/api/org`
- `curl -s -H 'Authorization: Bearer $GRAFANA_API_KEY' http://localhost:3000/api/search?type=dash-db | jq '.[].title'`
- `curl -s -X POST -H 'Authorization: Bearer $GRAFANA_API_KEY' -H 'Content-Type: application/json' http://localhost:3000/api/dashboards/db -d @dashboard.json`
- `curl -s -H 'Authorization: Bearer $GRAFANA_API_KEY' http://localhost:3000/api/datasources`
- `curl -s -X POST -H 'Authorization: Bearer $GRAFANA_API_KEY' -H 'Content-Type: application/json' -d '{"text":"deploy v2.14.3"}' http://localhost:3000/api/annotations`

**Examples:**
- curl -s -H 'Authorization: Bearer $KEY' http://localhost:3000/api/dashboards/uid/cQx8-abc | jq '.dashboard.title'
- curl -s -H 'Authorization: Bearer $KEY' 'http://localhost:3000/api/datasources' | jq '.[] | {name, type}'
- curl -s -X DELETE -H 'Authorization: Bearer $KEY' http://localhost:3000/api/datasources/uid/$DS_UID
