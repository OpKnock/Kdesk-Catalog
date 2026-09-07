---
type: agent_requested
description: "Apply timeouts at every layer of the call stack: HTTP client connect/read deadlines with curl and requests, gRPC deadlines with grpcurl, and proxy timeouts in nginx. Establishes a timeout ladder (client < proxy < backend) so hung downstreams fail fast without burning worker pools. Use when working with timeout application, api or when the user mentions timeout application, api."
---

Apply timeouts at every layer of the call stack: HTTP client connect/read deadlines with curl and requests, gRPC deadlines with grpcurl, and proxy timeouts in nginx. Establishes a timeout ladder (client < proxy < backend) so hung downstreams fail fast without burning worker pools.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl --connect-timeout 5 --max-time 15 http://localhost:8080`
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

# Timeout Pattern

Hand-crafted skill for bounding call durations end to end.

## What this skill does

- Sets connect and total timeouts on HTTP clients
- Applies gRPC deadlines for RPC calls
- Configures proxy timeouts so backends cannot hang forever

## When to use

- A downstream API occasionally hangs and burns workers
- Proxies keep connections open to dead backends
- Adding timeout hygiene to a service before load

## Real commands

```bash
# curl: 5s connect, 15s total
curl --connect-timeout 5 --max-time 15 https://api.example.com/slow

# gRPC: 10s deadline
grpcurl -max-time 10 -d '{}' localhost:8080 svc.Health.Check

# Python requests: connect + read timeouts
python -c 'import requests; requests.get("https://api.example.com", timeout=(3.05, 15))'

# Measure what the endpoint actually takes
curl -s -o /dev/null -w '%{http_code} %{time_total}\n' https://api.example.com/health
```

## nginx config

```nginx
location /api/ {
  proxy_connect_timeout 5s;
  proxy_send_timeout 30s;
  proxy_read_timeout 30s;
}
```

## Timeout ladder

- connect: 2-5s, first byte: 5-10s, total: 15-30s
- gRPC deadlines slightly above expected p99 latency
- Proxy read timeout longer than the slowest valid response

## Testing

```bash
# Simulate a hang with a slow endpoint, then:
curl --connect-timeout 5 --max-time 15 https://api.example.com/slow
```

## Best practices

- Always set both connect and total timeouts
- Return 504 from proxies when the backend times out
- Timeouts should ladder: client < proxy < backend

## Capabilities

### timeout-application
Apply timeouts at client, proxy, and application layers

**Parameters:**
- `connect_timeout` (integer): Seconds to establish the connection
- `total_timeout` (integer): Seconds for the whole call
- `layer` (string): client, proxy, or application

**Commands:**
- `curl --connect-timeout 5 --max-time 15 http://localhost:8080/slow`
- `grpcurl -max-time 10 -d '{}' localhost:8080 svc.Health.Check`
- `python -c 'import requests; requests.get("http://localhost:8080", timeout=(3.05, 15))'`
- `curl -s -o /dev/null -w '%{http_code} %{time_total}\n' http://localhost:8080/health`

**Examples:**
- curl --connect-timeout 5 --max-time 15 http://localhost:8080/slow
- grpcurl -max-time 10 -d '{}' localhost:8080 svc.Health.Check
- python -c 'import requests; requests.get("http://localhost:8080", timeout=(3.05, 15))'

## References
- [nginx proxy module timeouts](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_read_timeout)
- [curl timeouts](https://curl.se/docs/manpage.html#--max-time)