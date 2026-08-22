---
name: "health-check-engineer"
description: "Designs liveness/readiness probes and external health checks: curl probes, TCP listeners, and uptime verification for services."
type: knowledge
triggers: ["health-check-engineer", "http-probes", "tcp-ports"]
---

# health-check-engineer

Designs liveness/readiness probes and external health checks: curl probes, TCP listeners, and uptime verification for services.

## Instructions

# Health Checks

Design and operate liveness, readiness, and dependency probes.

## When to Use

- Adding /healthz and /readyz endpoints to services
- Diagnosing why a service is not receiving traffic
- Monitoring external uptime and DNS/TLS health

## Probe endpoints

- `/livez`: process is alive - fail only on fatal state.
- `/readyz`: can serve traffic - fail when dependencies are down.
- `/healthz`: deep check - DB, caches, external deps.

## Curl basics

```bash
curl -fsS http://localhost:8080/healthz
curl -s -o /dev/null -w '%{http_code} %{time_total}s\n' http://localhost:8080/readyz
```

Use `-f` to fail on 4xx/5xx, `-sS` to keep errors visible, and `-m 2` for a 2s deadline.

## TCP probes

```bash
nc -zv localhost 5432
openssl s_client -connect db.internal:5432 -brief </dev/null
```

## Kubernetes wiring

```yaml
livenessProbe:
  httpGet: { path: /livez, port: 8080 }
  initialDelaySeconds: 5
  periodSeconds: 10
readinessProbe:
  httpGet: { path: /readyz, port: 8080 }
  periodSeconds: 5
```

## Best practices

- Keep liveness probes dependency-free - a DB outage should not restart pods.
- Timeout probe calls; a hung probe is a false alarm.
- Log probe results and alert on error-rate spikes.
- Expose both TCP and HTTP probes where the platform supports them.

## Testing

```bash
curl -fsS --retry 3 --retry-all-errors http://localhost:8080/healthz
```

Simulate dependency failure and verify readyz flips before livez does.

## Capabilities

### http-probes
Probe HTTP endpoints and validate status, latency, and response bodies.

**Commands:**
- `curl -fsS http://localhost:8080/healthz`
- `curl -s -o /dev/null -w '%{http_code} %{time_total}s\n' http://localhost:8080/readyz`
- `curl -fsS -X POST -H 'Content-Type: application/json' -d '{"probe":"deep"}' http://localhost:8080/livez`
- `curl -fsS http://localhost:8080/healthz && echo 'UP' || echo 'DOWN'`
- `curl -fsS --retry 3 --retry-delay 5 --retry-all-errors http://localhost:8080/healthz`

**Examples:**
- curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8080/readyz
- curl -fsS -m 2 http://localhost:8080/healthz
- curl -fsS http://localhost:8080/healthz | jq -e '.status == "ok"'

### tcp-ports
Check TCP and TLS connectivity to services.

**Commands:**
- `nc -zv localhost 5432`
- `nc -z -w 3 localhost 3306 && echo 'port open'`
- `openssl s_client -connect db.internal:5432 -brief </dev/null`
- `tcping localhost 8080`
- `timeout 5 bash -c '</dev/tcp/localhost/6379' && echo 'redis up'`

**Examples:**
- nc -zvw 3 db.internal 5432
- openssl s_client -connect api.internal:443 -brief </dev/null
- nc -z localhost 27017 && echo 'mongo reachable'
