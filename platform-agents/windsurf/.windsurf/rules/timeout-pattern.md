---
trigger: glob
description: "Apply timeouts at every layer of the call stack: HTTP client connect/read deadlines with curl and requests, gRPC deadlines with grpcurl, and proxy timeouts in nginx. Establishes a timeout ladder (client < proxy < backend) so hung downstreams fail fast without burning worker pools."
globs: ["**/*.py", "**/*.r", "**/*.sh"]
---

# Timeout Pattern

Apply timeouts at every layer of the call stack: HTTP client connect/read deadlines with curl and requests, gRPC deadlines with grpcurl, and proxy timeouts in nginx. Establishes a timeout ladder (client < proxy < backend) so hung downstreams fail fast without burning worker pools.

## Instructions

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

**Commands:**
- `curl --connect-timeout 5 --max-time 15 http://localhost:8080/slow`
- `grpcurl -max-time 10 -d '{}' localhost:8080 svc.Health.Check`
- `python -c 'import requests; requests.get("http://localhost:8080", timeout=(3.05, 15))'`
- `curl -s -o /dev/null -w '%{http_code} %{time_total}\n' http://localhost:8080/health`

**Examples:**
- curl --connect-timeout 5 --max-time 15 http://localhost:8080/slow
- grpcurl -max-time 10 -d '{}' localhost:8080 svc.Health.Check
- python -c 'import requests; requests.get("http://localhost:8080", timeout=(3.05, 15))'
