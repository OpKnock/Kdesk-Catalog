# Log Aggregation

Collect logs from many sources into one place: Fluent Bit pipelines, journald/tail forwarding, and Kubernetes pod log collection.

## Instructions

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

**Commands:**
- `journalctl -u myapp --since '30 min ago' -f`
- `docker logs --tail 100 -f nginx`
- `kubectl logs --all-containers=true --since=1h deploy/api`
- `tail -f /var/log/app/app.log | logger -t app -p user.info`

**Examples:**
- journalctl -u myapp --since '30 min ago' -f
- kubectl logs --all-containers=true --since=1h deploy/api
- docker logs --tail 100 -f nginx
