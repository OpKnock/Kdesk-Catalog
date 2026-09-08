---
name: "haproxy"
description: "Configures and operates HAProxy: config validation, hot reloads, and runtime inspection via the stats socket. Use when working with config, stats, infrastructure or when the user mentions config, stats, infrastructure."
type: knowledge
triggers: ["haproxy", "config", "stats"]
---

Configures and operates HAProxy: config validation, hot reloads, and runtime inspection via the stats socket.

## Agentic Workflow: Read -> Reason -> Act (haproxy)

You are **Haproxy** (infrastructure/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — infrastructure context for `haproxy`
- Domain: Configures and operates HAProxy: config validation, hot reloads, and runtime inspection via the stats socket.
- **config**: Validate and reload HAProxy configuration. — `haproxy -c -f /etc/haproxy/haproxy.cfg`
- **stats**: Inspect runtime state via the admin socket. — `echo 'show info' | socat /run/haproxy/admin.sock -`
- Check `knowledge` and `prerequisites: echo, haproxy`

### 2. Reason — think for `haproxy`
- For `config`: Validate and reload HAProxy configuration. — decide which checks to run
- For `stats`: Inspect runtime state via the admin socket. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `haproxy` tools
- Tools: `Glob`, `Grep`, `Read`, `Haproxy`, `Echo` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `haproxy:0557dfe1`

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
