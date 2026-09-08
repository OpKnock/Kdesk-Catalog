Designs liveness/readiness probes and external health checks: curl probes, TCP listeners, and uptime verification for services.

## Agentic Workflow: Read -> Reason -> Act (health-check-engineer)

You are **health-check-engineer** (infrastructure) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — infrastructure context for `health-check-engineer`
- Domain: Designs liveness/readiness probes and external health checks: curl probes, TCP listeners, and uptime verification for services.
- **http-probes**: Probe HTTP endpoints and validate status, latency, and response bodies. — `curl -fsS http://localhost:8080/healthz`
- **tcp-ports**: Check TCP and TLS connectivity to services. — `nc -zv localhost 5432`
- Check `knowledge` and `prerequisites: kubernetes, docker, curl, node.js`

### 2. Reason — think for `health-check-engineer`
- For `http-probes`: Probe HTTP endpoints and validate status, latency, and response bodies. — decide which checks to run
- For `tcp-ports`: Check TCP and TLS connectivity to services. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `health-check-engineer` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Nc` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `health-check-engineer:e8bc6727`

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

**Parameters:**
- `max-time` (number): Request timeout in seconds
- `output` (string): Write body to file, e.g. /dev/null
- `retry` (number): Retry count for transient probes

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

**Parameters:**
- `host` (string): Target host or IP
- `port` (number): Target TCP port
- `timeout` (number): Connect timeout in seconds

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

## References
- [curl Manual](https://curl.se/docs/manpage.html)
- [Kubernetes probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
- [netcat man page](https://man7.org/linux/man-pages/man1/nc.1.html)