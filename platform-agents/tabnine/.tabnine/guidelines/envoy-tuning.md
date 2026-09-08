Envoy proxy tuning: inspect listeners, clusters, and endpoints via admin API; tune buffer, timeout, and connection pool settings.

## Agentic Workflow: Read -> Reason -> Act (envoy-tuning)

You are **Envoy Tuning** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `envoy-tuning`
- Domain: Envoy proxy tuning: inspect listeners, clusters, and endpoints via admin API; tune buffer, timeout, and connection pool settings.
- **envoy-admin**: Query the Envoy admin API for listeners, clusters, and stats, and drain or reset connections. — `curl -s http://localhost:15000/listeners | jq`
- Check `knowledge` references before acting

### 2. Reason — think for `envoy-tuning`
- For `envoy-admin`: Query the Envoy admin API for listeners, clusters, and stats, and drain or reset connections. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `envoy-tuning` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `envoy-tuning:c2832f27`

# Envoy Tuning

## What this skill does

Envoy is a high-performance L7 proxy. Tuning means reading the admin API for listener/cluster state, watching upstream latency stats, and adjusting connection pools, timeouts, and buffer sizes.

## When to use

- Latency regressions through a gateway or mesh sidecar
- Upstreams marked unhealthy or connection pool saturation
- Pre-launch capacity tuning

## Real commands

```bash
# What listeners exist
curl -s http://localhost:15000/listeners | jq '.[].name'

# Healthy endpoints per cluster
curl -s http://localhost:15000/clusters?format=json | jq '.cluster_statuses[] | {name: .name, membership: .membership.total_healthy_count}'

# Upstream latency percentiles
curl -s http://localhost:15000/stats?filter=cluster.orders.upstream_rq_time | grep -E 'P50|P95'

# Drain before a restart
curl -s -X POST http://localhost:15000/drain_listeners?inboundonly

# Zero out stats after a change
curl -s -X POST http://localhost:15000/reset_counters
```

## Tuning config example

```yaml
clusters:
  - name: orders
    connect_timeout: 1.5s
    circuit_breakers:
      thresholds:
        - max_connections: 1024
          max_pending_requests: 1024
          max_requests: 2048
    http2_protocol_options: {}
    health_checks:
      healthy_threshold: 2
      unhealthy_threshold: 3
      timeout: 1s
      interval: 5s
```

## Key stats

- `upstream_rq_time` P95: endpoint latency as seen by Envoy
- `upstream_cx_total` and `upstream_rq_pending_total`: pool saturation
- `upstream_cx_connect_fail`: network reachability

## Best practices

- Compare P50 vs P95; a widening gap points to queueing, not the endpoint.
- Tune one variable at a time and reset_counters between tests.
- Drain listeners before rolling a proxy to avoid connection resets.
- Keep connect_timeout short (1-2s); raise only for slow-start endpoints.

## Capabilities

### envoy-admin
Query the Envoy admin API for listeners, clusters, and stats, and drain or reset connections.

**Parameters:**
- `admin-port` (integer): Envoy admin port (default 15000 in Istio, 9901 standalone)
- `cluster-name` (string): Cluster name for stats filters
- `filter` (string): Stats filter regex

**Commands:**
- `curl -s http://localhost:15000/listeners | jq`
- `curl -s http://localhost:15000/clusters?format=json | jq '.cluster_statuses[] | {name: .name, membership: .membership.total_healthy_count}'`
- `curl -s http://localhost:15000/stats?filter=cluster.orders.upstream_rq_time | grep -E 'P50|P95'`
- `curl -s -X POST http://localhost:15000/drain_listeners?inboundonly`
- `curl -s -X POST http://localhost:15000/reset_counters`

**Examples:**
- curl -s http://localhost:15000/clusters?format=json | jq '.cluster_statuses[] | {name: .name, membership: .membership.total_healthy_count}'
- curl -s http://localhost:15000/stats?filter=cluster.orders.upstream_rq_time | grep -E 'P50|P95'
- curl -s http://localhost:15000/listeners | jq '.[].name'

## References
- [Envoy Admin Interface](https://www.envoyproxy.io/docs/envoy/latest/operations/admin)
- [Envoy Tuning Guide](https://www.envoyproxy.io/docs/envoy/latest/faq/performance/how_to_benchmark_envoy)