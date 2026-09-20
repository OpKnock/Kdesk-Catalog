---
trigger: glob
description: "Architects layer 4/7 load balancing with HAProxy and Envoy: routing, health checks, and capacity verification with load tools. Use when working with envoy, capacity or when the user mentions envoy, capacity."
globs: ["**/*.go", "**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

Architects layer 4/7 load balancing with HAProxy and Envoy: routing, health checks, and capacity verification with load tools.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `envoy -c envoy.yaml`, `hey -n 5000 -c 100 http://127.0.0.1:8080/`
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

# Load Balancer Engineering

Design and verify layer 4/7 balancers for capacity and correctness.

## When to Use

- Routing traffic across service instances
- TLS termination and header manipulation
- Capacity verification before launches

## Envoy basics

```yaml
static_resources:
  listeners:
    - name: listener_0
      address: { socket_address: { address: 0.0.0.0, port_value: 10000 } }
      filter_chains:
        - filters:
            - name: envoy.filters.network.http_connection_manager
              typed_config:
                "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
                stat_prefix: ingress
                route_config:
                  virtual_hosts:
                    - name: backend
                      domains: ["*"]
                      routes:
                        - match: { prefix: / }
                          route: { cluster: service_api }
                http_filters:
                  - name: envoy.filters.http.router
                    typed_config: { "@type": type.googleapis.com/envoy.extensions.filters.http.router.v3.Router }
  clusters:
    - name: service_api
      type: STRICT_DNS
      lb_policy: ROUND_ROBIN
      load_assignment:
        cluster_name: service_api
        endpoints:
          - lb_endpoints:
              - endpoint: { address: { socket_address: { address: api-1, port_value: 8080 } } }
```

```bash
envoy --mode validate --config-path envoy.yaml
envoy -c envoy.yaml
```

## Health and stats

```bash
curl -s http://127.0.0.1:9901/clusters | grep -E 'health_flags|healthy'
curl -s http://127.0.0.1:9901/stats/prometheus | grep 'envoy_cluster_upstream_cx_active'
```

## Capacity verification

```bash
ab -n 10000 -c 200 -k http://127.0.0.1:8080/
hey -n 5000 -c 100 http://127.0.0.1:8080/
```

Check: requests/sec, p95 latency, error rate, and backend saturation.

## Design decisions

- L4 (TCP passthrough) when the app handles TLS.
- L7 (Envoy/HAProxy) when routing on headers/paths.
- Always include health checks and a drain policy.

## Best practices

- Validate configs before every reload.
- Keep admin endpoints internal-only.
- Set graceful drain windows matching connection lifetime.
- Load test at 2x peak to find the failure curve.

## Testing

```bash
envoy --mode validate --config-path envoy.yaml
ab -n 10000 -c 200 -k http://127.0.0.1:8080/
```

Record the capacity baseline per release.

## Capabilities

### envoy
Configure and run Envoy proxies.

**Parameters:**
- `config-path` (string): Envoy bootstrap config file
- `mode` (string): validate or serve mode
- `admin-port` (number): Envoy admin listener port

**Commands:**
- `envoy -c envoy.yaml`
- `envoy --config-path envoy.yaml --mode validate`
- `envoy --mode validate --config-path envoy.yaml`
- `curl -s http://127.0.0.1:9901/stats | grep -E 'cluster.upstream_cx_active|http.downstream_rq_total'`
- `curl -s http://127.0.0.1:9901/clusters | grep -E 'health_flags|healthy'`

**Examples:**
- envoy --mode validate --config-path envoy.yaml
- curl -s http://127.0.0.1:9901/stats/prometheus | grep 'envoy_cluster_upstream_cx_active'
- curl -s http://127.0.0.1:9901/server_info | jq '.version'

### capacity
Verify balancer capacity with load generation.

**Parameters:**
- `requests` (number): Total request count
- `concurrency` (number): Concurrent connections
- `method` (string): HTTP method and payload

**Commands:**
- `hey -n 5000 -c 100 http://127.0.0.1:8080/`
- `ab -n 10000 -c 200 -k http://127.0.0.1:8080/api`
- `curl -sI http://127.0.0.1:8080/ | grep -iE 'HTTP|x-request-id'`
- `hey -n 2000 -c 50 -m POST -T 'application/json' -d '{"q":1}' http://127.0.0.1:8080/search`
- `curl -s -o /dev/null -w '%{time_total} %{http_code}\n' http://127.0.0.1:8080/healthz`

**Examples:**
- ab -n 10000 -c 200 -k http://127.0.0.1:8080/ | grep -E 'Requests per second|Failed requests'
- hey -n 3000 -c 100 -z 30s http://127.0.0.1:8080/
- curl -sI -H 'Host: api.example.com' http://127.0.0.1:8080/ | head -5

## References
- [Envoy Proxy Docs](https://www.envoyproxy.io/docs)
- [Envoy Admin API](https://www.envoyproxy.io/docs/envoy/latest/operations/admin)
- [HAProxy Management](https://www.haproxy.org/download/2.9/doc/management.txt)
