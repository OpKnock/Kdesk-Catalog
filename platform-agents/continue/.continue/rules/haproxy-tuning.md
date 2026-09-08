---
name: "Haproxy Tuning"
description: "HAProxy performance tuning: config validation, runtime stats via the socket, maxconn adjustments, keepalive tuning, and connection limits. Use when working with haproxy tuning, api or when the user mentions haproxy tuning, api."
globs: ["**/*.r", "**/*.sh"]
alwaysApply: false
---

HAProxy performance tuning: config validation, runtime stats via the socket, maxconn adjustments, keepalive tuning, and connection limits.

## Agentic Workflow: Read -> Reason -> Act (haproxy-tuning)

You are **Haproxy Tuning** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `haproxy-tuning`
- Domain: HAProxy performance tuning: config validation, runtime stats via the socket, maxconn adjustments, keepalive tuning, and connection limits.
- **haproxy-tuning**: Validate, start, and tune HAProxy using config checks and the stats socket. — `haproxy -c -f /etc/haproxy/haproxy.cfg`
- Check `knowledge` and `prerequisites: echo, haproxy`

### 2. Reason — think for `haproxy-tuning`
- For `haproxy-tuning`: Validate, start, and tune HAProxy using config checks and the stats socket. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `haproxy-tuning` tools
- Tools: `Glob`, `Grep`, `Read`, `Haproxy`, `Echo` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `haproxy-tuning:d49c525b`

# HAProxy Tuning

Tune HAProxy for throughput, latency, and connection behavior.

## What this skill does

- Validates configuration before reloads.
- Reads live counters (rate, connections, queues) from the runtime socket.
- Adjusts maxconn, timeouts, and server weights without restarting.
- Inspects server state for drain/maintenance operations.

## When to use

- Connections queue up behind a backend.
- Tuning maxconn to match kernel limits and backend capacity.
- Gradual draining of servers for maintenance.

## Real commands

```bash
# Validate config without starting
haproxy -c -f /etc/haproxy/haproxy.cfg

# Start in daemon mode with PID file
haproxy -f /etc/haproxy/haproxy.cfg -D -p /run/haproxy.pid

# Runtime stats
echo 'show info' | socat stdio /var/run/haproxy.sock
echo 'show stat' | socat stdio /var/run/haproxy.sock

# Runtime tuning
echo 'set maxconn 6000' | socat stdio /var/run/haproxy.sock
echo 'set timeout client 60s' | socat stdio /var/run/haproxy.sock

# Drain a backend server
echo 'set server web/web1 state drain' | socat stdio /var/run/haproxy.sock
```

## Tuning directives (haproxy.cfg)

```haproxy
global
  maxconn 5000
  tune.bufsize 32768
  tune.maxrewrite 1024

defaults
  timeout connect 5s
  timeout client 30s
  timeout server 30s
  timeout queue 10s
  maxconn 1000

backend web
  balance roundrobin
  server web1 10.0.0.11:8080 maxconn 500 weight 1
  server web2 10.0.0.12:8080 maxconn 500 weight 2
```

## Testing

```bash
# Watch connection growth during a load test
watch -n 1 "echo 'show info' | socat stdio /var/run/haproxy.sock | grep -E 'CurrConns|Maxconn'"
```

## Best practices

- Raise `ulimit -n` and `net.core.somaxconn` before maxconn.
- Use `maxconn` per server so one slow backend cannot monopolize the queue.
- Prefer `timeout queue` over letting clients wait forever.
- Validate with `haproxy -c` in CI before every deploy.

## Example exchange

```
User: Requests queue at 500+ during traffic spikes.
Agent: Raise maxconn, check backend server maxconn, and add timeout queue:
       echo 'set maxconn 10000' | socat stdio /var/run/haproxy.sock
```

## Capabilities

### haproxy-tuning
Validate, start, and tune HAProxy using config checks and the stats socket.

**Parameters:**
- `config_file` (string): Path to haproxy.cfg.
- `stats_socket` (string): Path to the admin socket, e.g. /var/run/haproxy.sock.
- `maxconn` (integer): Global connection limit to set at runtime.

**Commands:**
- `haproxy -c -f /etc/haproxy/haproxy.cfg`
- `haproxy -f /etc/haproxy/haproxy.cfg -D -p /run/haproxy.pid`
- `echo 'show info' | socat stdio /var/run/haproxy.sock`
- `echo 'show stat' | socat stdio /var/run/haproxy.sock`
- `echo 'set maxconn 6000' | socat stdio /var/run/haproxy.sock`

**Examples:**
- echo 'show servers state' | socat stdio /var/run/haproxy.sock
- echo 'set timeout client 60s' | socat stdio /var/run/haproxy.sock
- haproxy -c -f /etc/haproxy/haproxy.cfg -f /etc/haproxy/errors/ -d

## References
- [HAProxy Configuration Manual](https://docs.haproxy.org/current/configuration.html)
- [HAProxy Runtime API](https://docs.haproxy.org/current/management.html)