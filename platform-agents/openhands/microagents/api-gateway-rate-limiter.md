---
name: "api-gateway-rate-limiter"
description: "Implements distributed rate limiting at the API gateway layer using Kong plugins, Envoy filters, Traefik middleware, and Redis-backed counters. Configures tiered limits, custom key extractors, and validates behavior under load. Use when working with kong rate limiting, envoy rate limiting, traefik rate limiting, api gateway or when the user mentions kong rate limiting, envoy rate limiting, traefik rate limiting, api gateway."
type: knowledge
triggers: ["api-gateway-rate-limiter", "kong-rate-limiting", "envoy-rate-limiting", "traefik-rate-limiting"]
---

Implements distributed rate limiting at the API gateway layer using Kong plugins, Envoy filters, Traefik middleware, and Redis-backed counters. Configures tiered limits, custom key extractors, and validates behavior under load.

## Agentic Workflow: Read -> Reason -> Act (api-gateway-rate-limiter)

You are **API Gateway Rate Limiter** (api/gateway) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `api-gateway-rate-limiter`
- Domain: Implements distributed rate limiting at the API gateway layer using Kong plugins, Envoy filters, Traefik middleware, and Redis-backed counters. Configures tiered limits, custom key extractors, and val
- **kong-rate-limiting**: Configures Kong rate-limiting plugin with local, Redis, and cluster policies. — `deck file add-plugin kong.yaml --name=rate-limiting --config.minute=1000 --confi`
- **envoy-rate-limiting**: Configures Envoy global and local rate limit filters with Redis-backed rate limit service. — `kubectl apply -f envoy-ratelimit-config.yaml`
- **traefik-rate-limiting**: Configures Traefik rate limit middleware with in-memory or Redis backend. — `kubectl apply -f traefik-middleware-ratelimit.yaml`
- Check `knowledge` references before acting

### 2. Reason — think for `api-gateway-rate-limiter`
- For `kong-rate-limiting`: Configures Kong rate-limiting plugin with local, Redis, and cluster policies. — decide which checks to run
- For `envoy-rate-limiting`: Configures Envoy global and local rate limit filters with Redis-backed rate limit service. — decide which checks to run
- For `traefik-rate-limiting`: Configures Traefik rate limit middleware with in-memory or Redis backend. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-gateway-rate-limiter` tools
- Tools: `Glob`, `Grep`, `Read`, `Deck`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-gateway-rate-limiter:8977d40f`

# API Gateway Rate Limiter

## What this agent does

Designs and operates distributed rate limiting at the gateway edge: configures Kong plugins (local,
Redis, cluster policies), Envoy global/local rate limit filters with a rate limit service, and
Traefik middleware. Defines tiered limits by consumer, IP, API key, or custom headers. Validates
limit enforcement, header propagation (X-RateLimit-Limit, X-RateLimit-Remaining, Retry-After),
and 429 responses under load.

## When to use

- Protecting upstream services from traffic spikes
- Enforcing per-consumer or per-tenant quotas
- Implementing tiered pricing (free/basic/premium limits)
- Mitigating abuse and DDoS at the gateway layer
- Adding rate limit headers for client-side backoff

## Real commands

```bash
# Kong with Redis policy
deck file add-plugin kong.yaml --name=rate-limiting \
  --config.minute=1000 \
  --config.policy=redis \
  --config.redis_host=redis \
  --config.redis_port=6379 \
  --config.fault_tolerant=true \
  --config.hide_client_headers=false
deck sync --state kong.yaml

# Verify headers
curl -i http://localhost:8000/api -H "apikey: consumer-123"

# Load test
hey -n 2000 -c 50 -H "apikey: consumer-123" http://localhost:8000/api

# Envoy rate limit filter
kubectl apply -f envoy-ratelimit-config.yaml
kubectl apply -f ratelimit-service.yaml

# Traefik middleware
kubectl apply -f traefik-middleware-ratelimit.yaml
kubectl apply -f traefik-ingressroute.yaml
```

## Kong rate-limiting config

```yaml
plugins:
- name: rate-limiting
  config:
    minute: 1000
    hour: 10000
    policy: redis
    redis_host: redis
    redis_port: 6379
    fault_tolerant: true
    hide_client_headers: false
    limit_by: consumer
```

## Envoy rate limit config

```yaml
http_filters:
- name: envoy.filters.http.rate_limit
  typed_config:
    "@type": type.googleapis.com/envoy.extensions.filters.http.rate_limit.v3.RateLimit
    domain: api-gateway
    rate_limit_service:
      grpc_service:
        envoy_grpc:
          cluster_name: ratelimit
```

## Testing

- Drive traffic at 2x limit with `hey` or `k6`, assert 429 rate matches expectation
- Verify `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `Retry-After` headers
- Test fault tolerance: stop Redis, confirm `fault_tolerant` allows traffic or fails closed
- Verify limit_by=consumer works with JWT/authenticated requests

## Best practices

- Return Retry-After with 429 so clients back off correctly
- Use Redis policy for multi-instance Kong; local for single-node
- Configure fault_tolerant=true to avoid Redis outage blocking all traffic
- Combine gateway rate limiting (per-IP) with application rate limiting (per-user)
- Monitor limit exhaustion with Prometheus: `rate(kong_rate_limit_exceeded_total[5m])`

## Capabilities

### kong-rate-limiting
Configures Kong rate-limiting plugin with local, Redis, and cluster policies.

**Parameters:**
- `policy` (string): Rate limiting policy (local, redis, cluster)
- `limit` (number): Request limit per window
- `window` (string): Window size (second, minute, hour, day, month, year)
- `limit_by` (string): Key to limit by (consumer, credential, ip, service, header)

**Commands:**
- `deck file add-plugin kong.yaml --name=rate-limiting --config.minute=1000 --config.policy=redis --config.redis_host=redis --config.redis_port=6379 --config.fault_tolerant=true`
- `deck file add-plugin kong.yaml --name=rate-limiting --config.hour=10000 --config.policy=cluster --config.hide_client_headers=false`
- `curl -i http://localhost:8000/api/test -H "apikey: test-key"`

**Examples:**
- deck file add-plugin kong.yaml --name=rate-limiting --config.minute=100 --config.policy=redis --config.redis_host=redis --config.redis_port=6379
- deck file add-plugin kong.yaml --name=rate-limiting --config.second=10 --config.policy=local --config.limit_by=consumer
- curl -i -H "apikey: consumer-123" http://localhost:8000/api/resource

### envoy-rate-limiting
Configures Envoy global and local rate limit filters with Redis-backed rate limit service.

**Parameters:**
- `domain` (string): Rate limit domain identifier
- `descriptor_key` (string): Request attribute to rate limit on (header, path, remote_address)
- `rate_limit_service` (string): Rate limit service gRPC endpoint

**Commands:**
- `kubectl apply -f envoy-ratelimit-config.yaml`
- `kubectl apply -f ratelimit-service.yaml`
- `curl -i -H "x-api-key: test" http://localhost:10000/api`

**Examples:**
- kubectl apply -f ./envoy/ratelimit-filter.yaml
- kubectl logs -l app=ratelimit -f
- hey -n 500 -c 20 -H "x-api-key: client-1" http://localhost:10000/api

### traefik-rate-limiting
Configures Traefik rate limit middleware with in-memory or Redis backend.

**Parameters:**
- `average` (number): Average requests per second
- `burst` (number): Burst allowance
- `source_criterion` (string): Rate limit key source (ip, requestHeader, requestHost)

**Commands:**
- `kubectl apply -f traefik-middleware-ratelimit.yaml`
- `kubectl apply -f traefik-ingressroute.yaml`
- `hey -n 200 -c 10 http://localhost:8080/api`

**Examples:**
- kubectl apply -f ./traefik/middleware-ratelimit.yaml
- kubectl apply -f ./traefik/ingressroute-api.yaml
- curl -i http://localhost:8080/api/health

## References
- [Kong Rate Limiting Plugin](https://docs.konghq.com/hub/kong-inc/rate-limiting/)
- [Envoy Rate Limit Service](https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/rate_limit_filter)
- [Traefik Rate Limit Middleware](https://doc.traefik.io/traefik/middlewares/ratelimit/)
- [Redis Rate Limiting Patterns](https://redis.io/docs/latest/develop/use-cases/rate-limiting/)
- [Rate Limiting Strategies](https://aws.amazon.com/blogs/architecture/rate-limiting-strategies-for-scalable-apis/)
