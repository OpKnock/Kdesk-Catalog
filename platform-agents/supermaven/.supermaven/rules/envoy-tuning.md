# Envoy Tuning

Envoy proxy tuning: inspect listeners, clusters, and endpoints via admin API; tune buffer, timeout, and connection pool settings.

## Instructions

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