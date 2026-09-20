---
name: "fluent-bit"
description: "Lightweight log and metric forwarding with Fluent Bit: configure inputs, parsers, and outputs, and validate configs before running."
type: knowledge
triggers: ["fluent-bit", "fluentbit-config"]
---

# Fluent Bit

Lightweight log and metric forwarding with Fluent Bit: configure inputs, parsers, and outputs, and validate configs before running.

## Instructions

# Fluent Bit

## What this skill does

Fluent Bit is a high-performance log/metric processor written in C, ideal for sidecars and edge agents. Config is declared in fluent-bit.conf with [SERVICE], [INPUT], [FILTER], and [OUTPUT] sections; the CLI overrides at runtime.

## When to use

- Tailing container logs to Elasticsearch/Loki
- Forwarding syslog from network devices
- Low-footprint logging on edge nodes

## Real commands

```bash
# Validate without running
fluent-bit --dry-run -c fluent-bit.conf

# Run with a config
fluent-bit -c fluent-bit.conf

# Quick inline pipeline: tail -> stdout
fluent-bit -i tail -p path=/var/log/app.log -o stdout -f 1

# Parsers at runtime
fluent-bit -R parsers.conf -i dummy -o stdout
```

## fluent-bit.conf example

```ini
[SERVICE]
    Flush 1
    Log_Level info

[INPUT]
    Name tail
    Path /var/log/app/*.log
    Parser json
    Tag app.*

[FILTER]
    Name rewrite_tag
    Match app.*
    Rule $log_level ^(ERROR|WARN)$ error.$TAG true

[OUTPUT]
    Name es
    Match *
    Host elasticsearch
    Port 9200
    Index app-logs
```

## Testing

```bash
# Watch the pipeline end to end
fluent-bit -i tail -p path=/tmp/demo.log -o stdout
# in another shell:
echo '{"log_level":"ERROR","msg":"boom"}' >> /tmp/demo.log
```

## Best practices

- Always run `--dry-run` in CI before deploying configs.
- Tag early, filter by tag, and route outputs by tag.
- Use built-in parsers (json, syslog, nginx) before writing custom regexes.
- Set reasonable Buffer_Size and Mem_Buf_Limit to avoid OOM on bursts.
- Test parser regexes with `fluent-bit -R parsers.conf -i dummy` offline.

## Capabilities

### fluentbit-config
Validate configs, run Fluent Bit with tail/forward inputs, and test outputs.

**Commands:**
- `fluent-bit --dry-run -c fluent-bit.conf`
- `fluent-bit -c fluent-bit.conf`
- `fluent-bit -i tail -p path=/var/log/app.log -o stdout -f 1`
- `fluent-bit -R parsers.conf -i dummy -o stdout`
- `fluent-bit --help | grep -A2 tail`

**Examples:**
- fluent-bit --dry-run -c fluent-bit.conf
- fluent-bit -i tail -p path=/var/log/app.log -o stdout -f 1
- fluent-bit -R parsers.conf -i dummy -o stdout
