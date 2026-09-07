---
type: agent_requested
description: "Configures and operates HAProxy: config validation, hot reloads, and runtime inspection via the stats socket. Use when working with config, stats, infrastructure or when the user mentions config, stats, infrastructure."
---

Configures and operates HAProxy: config validation, hot reloads, and runtime inspection via the stats socket.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `haproxy -c -f /etc/haproxy/haproxy.cfg`, `echo 'show info' | socat /run/haproxy/admin.sock -`
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

# HAProxy

Configure, reload, and operate HAProxy load balancers.

## When to Use

- Fronting web services with layer 4/7 load balancing
- Zero-downtime config changes
- Traffic control: drain, maintenance, and health checks

## Basic config

```haproxy
frontend web
  bind *:80
  default_backend servers

backend servers
  balance roundrobin
  option httpchk GET /healthz
  server web-1 10.0.1.11:8080 check inter 3s fall 3 rise 2
  server web-2 10.0.1.12:8080 check inter 3s fall 3 rise 2
```

## Validate before touching production

```bash
haproxy -c -f /etc/haproxy/haproxy.cfg
```

## Reload without dropping connections

```bash
haproxy -f /etc/haproxy/haproxy.cfg -p /run/haproxy.pid -sf $(cat /run/haproxy.pid)
```

`-sf` asks the old process to finish in-flight connections before exiting.

## Runtime control

```bash
echo 'show stat' | socat /run/haproxy/admin.sock - | grep 'web,'
echo 'set server web/web-1 state maint' | socat /run/haproxy/admin.sock -
echo 'set server web/web-1 state ready' | socat /run/haproxy/admin.sock -
```

## Diagnostics

```bash
echo 'show info' | socat /run/haproxy/admin.sock -
haproxy -vv
```

## Best practices

- Always validate config in CI before deploying.
- Enable `option log` with a local syslog endpoint.
- Use drain (not maint) for graceful node removal.
- Check the socket file permissions - it is an admin channel.

## Testing

```bash
haproxy -c -f /etc/haproxy/haproxy.cfg
echo 'show stat' | socat /run/haproxy/admin.sock - | grep DOWN
```

Simulate a server down and confirm the health check flips state.

## Capabilities

### config
Validate and reload HAProxy configuration.

**Parameters:**
- `c` (string): Check configuration only
- `f` (string): Config file path (repeatable)
- `sf` (string): Soft-stop old PIDs for reload

**Commands:**
- `haproxy -c -f /etc/haproxy/haproxy.cfg`
- `haproxy -f /etc/haproxy/haproxy.cfg -p /run/haproxy.pid -sf $(cat /run/haproxy.pid)`
- `haproxy -vv`
- `haproxy -f /etc/haproxy/haproxy.cfg -d`
- `haproxy -c -f /etc/haproxy/haproxy.cfg -C /etc/haproxy/errors`

**Examples:**
- haproxy -c -f haproxy.cfg -f haproxy-extra.cfg
- haproxy -vv | grep -E 'HA-Proxy version|OpenSSL'
- haproxy -f /etc/haproxy/haproxy.cfg -p /run/haproxy.pid -sf $(cat /run/haproxy.pid)

### stats
Inspect runtime state via the admin socket.

**Parameters:**
- `command` (string): Socket command: show stat, show info, set server
- `server` (string): backend/server pair, e.g. web/web-1
- `state` (string): drain, maint, or ready state

**Commands:**
- `echo 'show info' | socat /run/haproxy/admin.sock -`
- `echo 'show stat' | socat /run/haproxy/admin.sock -`
- `echo 'show servers state' | socat /run/haproxy/admin.sock -`
- `echo 'set server web/web-1 state maint' | socat /run/haproxy/admin.sock -`
- `echo 'show backend' | socat /run/haproxy/admin.sock -`

**Examples:**
- echo 'show stat' | socat /run/haproxy/admin.sock - | grep -E 'web,.*DOWN'
- echo 'set server web/web-2 state ready' | socat /run/haproxy/admin.sock -
- echo 'show info' | socat /run/haproxy/admin.sock - | grep -E 'CurrConns|Uptime'

## References
- [HAProxy Configuration Manual](https://www.haproxy.com/documentation/haproxy-configuration-manual/latest/)
- [HAProxy Management](https://www.haproxy.org/download/2.9/doc/management.txt)
- [HAProxy Stats Socket](https://docs.haproxy.org/2.9/management.html#9.3)