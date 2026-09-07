---
type: agent_requested
description: "Collect logs from many sources into one place: Fluent Bit pipelines, journald/tail forwarding, and Kubernetes pod log collection. Use when working with fluent bit, source forwarding, api or when the user mentions fluent bit, source forwarding, api."
---

Collect logs from many sources into one place: Fluent Bit pipelines, journald/tail forwarding, and Kubernetes pod log collection.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `fluent-bit -c fluent-bit.conf`, `journalctl -u myapp --since '30 min ago' -f`
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

# Log Aggregation

Centralize logs from hosts, containers, and clusters.

## What this skill does

- Runs Fluent Bit pipelines for tail/systemd/docker inputs.
- Forwards logs to central sinks (forward, elasticsearch, loki).
- Streams journald, docker, and k8s logs for debugging.

## When to use

- Building a central log store for audit and debugging.
- Routing app logs to observability platforms.
- Standardizing log collection across hosts.

## Real commands

```bash
# Fluent Bit: file -> stdout
fluent-bit -i tail -p path=/var/log/app.log -o stdout

# Fluent Bit: nginx access log -> fluent forward
fluent-bit -i tail -p path=/var/log/nginx/access.log \
  -o forward -p host=10.0.0.5 -p port=24224

# Fluent Bit: systemd unit
fluent-bit -i systemd -p systemd_filter=_SYSTEMD_UNIT=myapp.service -o stdout

# Config-file mode
fluent-bit -c fluent-bit.conf

# Direct streams
journalctl -u myapp --since '30 min ago' -f
docker logs --tail 100 -f nginx
kubectl logs --all-containers=true --since=1h deploy/api
tail -f /var/log/app/app.log | logger -t app -p user.info
```

## fluent-bit.conf example

```ini
[INPUT]
    Name tail
    Path /var/log/app/*.log
    Tag app.*

[OUTPUT]
    Name forward
    Match app.*
    Host 10.0.0.5
    Port 24224
```

## Testing

```bash
fluent-bit -i tail -p path=/var/log/app.log -o stdout --dry-run
```

## Best practices

- Tag logs by source so routing rules stay clean.
- Add parsers (nginx, json) at ingestion for structured fields.
- Buffer locally (file buffer) so outages don't drop logs.

## Capabilities

### fluent-bit
Run Fluent Bit with input/output pipelines.

**Parameters:**
- `input` (string): Input plugin: tail, systemd, docker, kube.
- `path` (string): Log file path for tail input.
- `output` (string): Output plugin: stdout, forward, elasticsearch, loki.

**Commands:**
- `fluent-bit -c fluent-bit.conf`
- `fluent-bit -i tail -p path=/var/log/app.log -o stdout`
- `fluent-bit -i tail -p path=/var/log/nginx/access.log -o forward -p host=10.0.0.5 -p port=24224`
- `fluent-bit -i systemd -p systemd_filter=_SYSTEMD_UNIT=myapp.service -o stdout`

**Examples:**
- fluent-bit -i tail -p path=/var/log/app.log -o stdout
- fluent-bit -i tail -p path=/var/log/nginx/access.log -o forward -p host=10.0.0.5 -p port=24224
- fluent-bit -i systemd -p systemd_filter=_SYSTEMD_UNIT=myapp.service -o stdout

### source-forwarding
Forward logs from journald, docker, and Kubernetes.

**Parameters:**
- `unit` (string): systemd unit name.
- `pod` (string): Kubernetes workload selector.

**Commands:**
- `journalctl -u myapp --since '30 min ago' -f`
- `docker logs --tail 100 -f nginx`
- `kubectl logs --all-containers=true --since=1h deploy/api`
- `tail -f /var/log/app/app.log | logger -t app -p user.info`

**Examples:**
- journalctl -u myapp --since '30 min ago' -f
- kubectl logs --all-containers=true --since=1h deploy/api
- docker logs --tail 100 -f nginx

## References
- [Fluent Bit Docs](https://docs.fluentbit.io/manual/)
- [journalctl man page](https://man7.org/linux/man-pages/man1/journalctl.1.html)