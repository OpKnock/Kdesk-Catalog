---
trigger: glob
description: "Envoy proxy. Real envoy CLI."
globs: ["**/*.go", "**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

# envoy

Envoy proxy. Real envoy CLI.

## Instructions

# Envoy Proxy

Envoy proxy using real CLI.

## When to Use

- Edge proxy
- Service mesh data plane
- Load balancing

## Commands

```bash
# Run Envoy
envoy -c envoy.yaml

# Validate config
envoy -c envoy.yaml --mode validate

# Hot reload
envoy -c envoy.yaml --restart-epoch 1

# View stats
curl http://localhost:9901/stats

# View config
curl http://localhost:9901/config_dump

# Ready check
curl http://localhost:9901/ready

# Server info
curl http://localhost:9901/server_info
```

## envoy.yaml

```yaml
static_resources:
  listeners:
    - name: listener_0
      address:
        socket_address:
          address: 0.0.0.0
          port_value: 8080
      filter_chains:
        - filters:
            - name: envoy.filters.network.http_connection_manager
              typed_config:
                "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
                stat_prefix: ingress_http
                route_config:
                  name: local_route
                  virtual_hosts:
                    - name: backend
                      domains: ["*"]
                      routes:
                        - match:
                            prefix: "/"
                          route:
                            cluster: upstream
                http_filters:
                  - name: envoy.filters.http.router
  clusters:
    - name: upstream
      connect_timeout: 0.25s
      type: STRICT_DNS
      load_assignment:
        cluster_name: upstream
        endpoints:
          - lb_endpoints:
              - endpoint:
                  address:
                    socket_address:
                      address: 127.0.0.1
                      port_value: 3000
```

## Admin Interface

```bash
# Stats
curl http://localhost:9901/stats

# Stats with prefix
curl http://localhost:9901/stats?filter=upstream

# Config dump
curl http://localhost:9901/config_dump

# Clusters
curl http://localhost:9901/clusters

# Ready
curl http://localhost:9901/ready

# Live
curl http://localhost:9901/server_info
```

## Filters

```yaml
http_filters:
  - name: envoy.filters.http.cors
    typed_config:
      "@type": type.googleapis.com/envoy.extensions.filters.http.cors.v3.Cors
  - name: envoy.filters.http.jwt_authn
    typed_config:
      "@type": type.googleapis.com/envoy.extensions.filters.http.jwt_authn.v3.JwtAuthentication
      providers:
        auth:
          issuer: https://auth.example.com
          audiences: ["api"]
          remote_jwks:
            http_uri:
              uri: https://auth.example.com/.well-known/jwks.json
              cluster: auth_cluster
              timeout: 5s
```

## Capabilities

### envoy
Envoy proxy. Real envoy CLI.

**Commands:**
- `envoy -c envoy.yaml`
- `envoy -c envoy.yaml --mode validate`
- `envoy -c envoy.yaml --restart-epoch 1`
- `curl http://localhost:9901/stats`
- `curl http://localhost:9901/config_dump`
- `curl http://localhost:9901/ready`
- `curl http://localhost:9901/server_info`
- `curl http://localhost:9901/stats`
- `curl http://localhost:9901/stats?filter=upstream`
- `curl http://localhost:9901/config_dump`
- `curl http://localhost:9901/clusters`
- `curl http://localhost:9901/ready`
- `curl http://localhost:9901/server_info`

**Examples:**
- envoy -c envoy.yaml
- envoy -c envoy.yaml --mode validate
- envoy -c envoy.yaml --restart-epoch 1
