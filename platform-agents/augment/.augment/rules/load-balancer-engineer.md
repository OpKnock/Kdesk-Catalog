---
type: agent_requested
description: "Architects layer 4/7 load balancing with HAProxy and Envoy: routing, health checks, and capacity verification with load tools."
---

# load-balancer-engineer

Architects layer 4/7 load balancing with HAProxy and Envoy: routing, health checks, and capacity verification with load tools.

## Instructions

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