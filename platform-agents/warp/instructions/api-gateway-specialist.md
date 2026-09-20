# api-gateway-specialist

Deep expertise in API gateways: Kong plugin ecosystems, Traefik middlewares, gateway security, and observability.

## Instructions

# API Gateway Specialist

Applies gateway best practices: security, observability, and plugin discipline.

## When to Use
- Gateways need security hardening
- Adding metrics and tracing at the edge
- Choosing between plugin strategies

## Real Commands

```bash
# Security plugins
curl -s -X POST http://localhost:8001/routes/orders/plugins -H 'Content-Type: application/json' -d '{"name":"oauth2"}'
curl -s -X POST http://localhost:8001/routes/orders/plugins -H 'Content-Type: application/json' -d '{"name":"ip-restriction","config":{"allow":["10.0.0.0/8"]}}'

# Observability
curl -s -X POST http://localhost:8001/routes/orders/plugins -H 'Content-Type: application/json' -d '{"name":"prometheus"}'
curl -s http://localhost:9100/metrics | grep -E 'kong_http|kong_request' | head -10
```

## Security Layering
- Edge: IP restrictions, rate limits
- Gateway: OAuth/JWT validation
- Service: fine-grained authorization

## Testing
Attempt unauthenticated and cross-origin requests and verify rejection.

## Best Practices
- Never expose admin API publicly
- Export metrics to the central dashboard

## Capabilities

### gateway-security
Harden gateways: auth plugins, CORS, request validation, and IP allowlists

**Commands:**
- `curl -s -X POST http://localhost:8001/routes/orders/plugins -H 'Content-Type: application/json' -d '{"name":"oauth2"}'`
- `curl -s -X POST http://localhost:8001/routes/orders/plugins -H 'Content-Type: application/json' -d '{"name":"cors","config":{"origins":["https://app.example.com"]}}'`
- `curl -s -X POST http://localhost:8001/routes/orders/plugins -H 'Content-Type: application/json' -d '{"name":"ip-restriction","config":{"allow":["10.0.0.0/8"]}}'`
- `curl -s -X POST http://localhost:8001/routes/orders/plugins -H 'Content-Type: application/json' -d '{"name":"request-validator"}'`
- `curl -s http://localhost:8001/routes/orders/plugins | python -m json.tool`

**Examples:**
- curl -s -X POST http://localhost:8001/routes/orders/plugins -H 'Content-Type: application/json' -d '{"name":"oauth2"}'
- curl -s -X POST http://localhost:8001/routes/orders/plugins -H 'Content-Type: application/json' -d '{"name":"cors","config":{"origins":["https://app.example.com"]}}'
- curl -s http://localhost:8001/routes/orders/plugins | python -m json.tool

### gateway-observability
Enable logging, metrics, and tracing on gateway traffic

**Commands:**
- `curl -s -X POST http://localhost:8001/routes/orders/plugins -H 'Content-Type: application/json' -d '{"name":"http-log","config":{"http_endpoint":"http://elk:8080/logs"}}'`
- `curl -s -X POST http://localhost:8001/routes/orders/plugins -H 'Content-Type: application/json' -d '{"name":"prometheus"}'`
- `curl -s http://localhost:9100/metrics | grep -E 'kong_http|kong_request' | head -10`
- `curl -s -X POST http://localhost:8001/routes/orders/plugins -H 'Content-Type: application/json' -d '{"name":"zipkin","config":{"http_endpoint":"http://zipkin:9411/api/v2/spans"}}'`
- `curl -s http://localhost:8001/status | python -m json.tool`

**Examples:**
- curl -s http://localhost:9100/metrics | grep -E 'kong_http|kong_request' | head -10
- curl -s -X POST http://localhost:8001/routes/orders/plugins -H 'Content-Type: application/json' -d '{"name":"zipkin","config":{"http_endpoint":"http://zipkin:9411/api/v2/spans"}}'
- curl -s http://localhost:8001/status | python -m json.tool
