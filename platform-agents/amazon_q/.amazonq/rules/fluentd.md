# Fluentd

Log collection with Fluentd: run the agent, configure input/output plugins, test configs, and manage buffers.

## Instructions

# Fluentd

## What this skill does

Fluentd is a Ruby-based log collector with a rich plugin ecosystem (in_tail, out_elasticsearch, out_s3). Events route via match patterns and buffer to smooth bursts. It exposes a monitoring agent on port 24220.

## When to use

- Centralized logging with heavy plugin needs
- Multi-format log ingestion (tail, forward, http)
- Routing logs to multiple destinations

## Real commands

```bash
# Validate config
fluentd --dry-run -c fluent.conf

# Run with custom plugins
fluentd -c fluent.conf -p /etc/fluent/plugin

# Plugin management
fluent-gem list | grep fluent-plugin
fluent-gem install fluent-plugin-elasticsearch

# Monitoring agent
curl -s http://localhost:24220/api/plugins.json | jq '.plugins[] | {plugin_id, type, emit_records}'
```

## fluent.conf example

```conf
<source>
  @type tail
  tag app.*
  path /var/log/app/*.log
  <parse>
    @type json
  </parse>
</source>

<filter app.**>
  @type record_transformer
  <record>
    host ${hostname}
  </record>
</filter>

<match app.**>
  @type elasticsearch
  host elasticsearch
  port 9200
  index_name app-logs
  <buffer>
    @type file
    path /var/log/fluentd/buffer
    flush_interval 5s
  </buffer>
</match>
```

## Testing

```bash
# Dry-run then watch metrics while producing logs
echo '{"msg":"hello"}' >> /var/log/app/test.log
curl -s http://localhost:24220/api/plugins.json | jq '.plugins[] | select(.type | contains("elasticsearch")) | .emit_records'
```

## Best practices

- Validate with --dry-run in CI for every config change.
- Use file buffers so crashes don't lose events.
- Watch the monitor agent's emit_records to detect stuck buffers.
- Match with the most specific tag pattern possible.
- Pin plugin versions in the Docker image.

## Capabilities

### fluentd-agent
Validate, run, and monitor Fluentd configurations and plugins.

**Commands:**
- `fluentd --dry-run -c fluent.conf`
- `fluentd -c fluent.conf -p /etc/fluent/plugin`
- `fluent-gem list | grep fluent-plugin`
- `fluent-gem install fluent-plugin-elasticsearch`
- `curl -s http://localhost:24220/api/plugins.json | jq '.plugins[] | {plugin_id, type, emit_records}'`

**Examples:**
- fluentd --dry-run -c fluent.conf
- curl -s http://localhost:24220/api/plugins.json | jq '.plugins[] | {plugin_id, type, emit_records}'
- fluent-gem install fluent-plugin-elasticsearch