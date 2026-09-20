---
applyTo: "**/*.r **/*.sh"
---

Endpoint health checking from the CLI: curl -f probes, TCP checks with nc, HTTP status verification, and Kubernetes readiness waits.

## Agentic Workflow: Read -> Reason -> Act (health-check)

You are **Health Check** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `health-check`
- Domain: Endpoint health checking from the CLI: curl -f probes, TCP checks with nc, HTTP status verification, and Kubernetes readiness waits.
- **endpoint-probing**: Probe HTTP and TCP endpoints for availability from scripts and CI. — `curl -f -s -o /dev/null -w '%{http_code}\n' http://localhost:8080/healthz`
- Check `knowledge` and `prerequisites: kubectl, wget`

### 2. Reason — think for `health-check`
- For `endpoint-probing`: Probe HTTP and TCP endpoints for availability from scripts and CI. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `health-check` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Nc` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `health-check:10a9c964`

# Health Check

Probe service health from the command line.

## What this skill does

- Checks HTTP health endpoints with curl and wget.
- Tests TCP reachability with nc.
- Waits for Kubernetes deployment readiness.
- Reports latency and status codes for alerting scripts.

## When to use

- Before restarting a service, confirm it is unhealthy.
- In CI, gate deploys on health endpoints.
- Debugging why a load balancer removed a backend.

## Real commands

```bash
# HTTP probe, fail on non-2xx, print code
curl -f -s -o /dev/null -w '%{http_code}\n' http://localhost:8080/healthz

# Simple OK check
curl -fsS http://localhost:8080/health && echo OK

# TCP reachability
nc -zv localhost 8080
nc -zv -w 3 localhost 5432

# Header inspection
wget --spider -S http://localhost:8080/health 2>&1 | grep HTTP

# Kubernetes readiness
kubectl wait --for=condition=Available deployment/web -n default --timeout=60s
```

## CI gate

```bash
if curl -fsS --max-time 5 http://localhost:8080/health > /dev/null; then
  echo "healthy"
else
  echo "unhealthy"; exit 1
fi
```

## Testing

```bash
# Latency check
curl -s -o /dev/null -w 'dns=%{time_namelookup} connect=%{time_connect} total=%{time_total}\n' http://localhost:8080/health
```

## Best practices

- Always set `--max-time`; never let probes hang.
- Use `-f` so non-2xx exits non-zero for scripts.
- Probe the health endpoint, not the homepage.
- Distinguish liveness (process up) from readiness (deps ready) in Kubernetes.

## Example exchange

```
User: Is the web service up?
Agent: curl -fsS http://localhost:8080/health && echo OK
       # prints OK when the service responds 2xx
```

## Capabilities

### endpoint-probing
Probe HTTP and TCP endpoints for availability from scripts and CI.

**Parameters:**
- `url` (string): Health endpoint URL.
- `timeout` (integer): Probe timeout in seconds.
- `expected_code` (integer): Expected HTTP status, default 200.

**Commands:**
- `curl -f -s -o /dev/null -w '%{http_code}\n' http://localhost:8080/healthz`
- `curl -fsS http://localhost:8080/health && echo OK`
- `nc -zv localhost 8080`
- `wget --spider -S http://localhost:8080/health 2>&1 | grep HTTP`
- `kubectl wait --for=condition=Available deployment/web -n default --timeout=60s`

**Examples:**
- curl -fsS --max-time 3 http://localhost:8080/health || exit 1
- nc -zv -w 3 localhost 5432
- curl -s -o /dev/null -w '%{time_total}\n' http://localhost:8080/health

## References
- [curl manual](https://curl.se/docs/manpage.html)
- [kubectl wait reference](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_wait/)
