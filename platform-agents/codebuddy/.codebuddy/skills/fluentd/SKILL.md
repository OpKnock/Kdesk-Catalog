---
name: "fluentd"
description: "Log collection with Fluentd: run the agent, configure input/output plugins, test configs, and manage buffers. Use when working with fluentd agent, api or when the user mentions fluentd agent, api."
license: "MIT"
compatibility: "Requires fluent-gem, fluentd. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(fluent-gem:*) Bash(fluentd:*)"
---

Log collection with Fluentd: run the agent, configure input/output plugins, test configs, and manage buffers.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `fluentd --dry-run -c fluent.conf`
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

**Parameters:**
- `config-file` (string): Path to fluent.conf
- `plugin-dir` (string): Custom plugin directory
- `monitor-port` (integer): Fluentd monitor agent port (default 24220)

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

## References
- [Fluentd docs](https://docs.fluentd.org/)
- [Fluentd buffer plugins](https://docs.fluentd.org/configuration/buffer-section)
