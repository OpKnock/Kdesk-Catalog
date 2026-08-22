---
trigger: glob
description: "Priority-aware rate limiting: separate limits for high/low-priority clients with Kong plugins and nginx maps."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

# Priority Rate Limiting

Priority-aware rate limiting: separate limits for high/low-priority clients with Kong plugins and nginx maps.

## Instructions

# Priority Rate Limiting

Not all clients are equal: grant premium/high-priority traffic more headroom than default tiers.

## What this skill does

- Applies tiered limits with Kong plugins per consumer
- Uses nginx map + limit_req for header-based tiers
- Verifies 429 behavior per tier

## When to use

- API plans with different quotas
- Protecting critical traffic during overload

## Real commands

```bash
# Kong: global plugin
curl -X POST http://localhost:8001/plugins -H "Content-Type: application/json" \
  -d '{"name":"rate-limiting","config":{"minute":60,"policy":"redis"}}'

# Kong: higher limit for a specific consumer
curl -X POST http://localhost:8001/consumers/priority-high/plugins \
  -H "Content-Type: application/json" -d '{"name":"rate-limiting","config":{"minute":600}}'

# Verify tier behavior
curl -s -o /dev/null -w "%{http_code}\n" -H "X-Priority: low" http://localhost:8080/api
curl -s -o /dev/null -w "%{http_code}\n" -H "X-Priority: high" http://localhost:8080/api
```

## nginx map approach

```nginx
map $http_x_priority $req_limit {
    default   10r/s;
    high      100r/s;
}
limit_req_zone $binary_remote_addr zone=api:10m rate=$req_limit;
```

## Best practices

- Return 429 with Retry-After header
- Use Redis policy when running multiple gateways
- Document tier limits in the developer portal

## Capabilities

### priority-rate-limiting
Enforce different rate limits per priority tier using Kong rate-limiting plugins and nginx map-based configs.

**Commands:**
- `curl -X POST http://localhost:8001/plugins -H "Content-Type: application/json" -d '{"name":"rate-limiting","config":{"minute":60,"policy":"redis"}}'`
- `curl -X POST http://localhost:8001/consumers/priority-high/plugins -H "Content-Type: application/json" -d '{"name":"rate-limiting","config":{"minute":600}}'`
- `curl -s http://localhost:8001/consumers | jq .`
- `curl -s -o /dev/null -w "%{http_code}\n" -H "X-Priority: low" http://localhost:8080/api`
- `curl -s -o /dev/null -w "%{http_code}\n" -H "X-Priority: high" http://localhost:8080/api`

**Examples:**
- curl -X POST http://localhost:8001/plugins -d '{"name":"rate-limiting","config":{"hour":1000,"policy":"local"}}'
- curl -s -o /dev/null -w "%{http_code}\n" -H "X-Priority: high" http://localhost:8080/api
- curl -X PATCH http://localhost:8001/plugins/PLUGIN_ID -d '{"config":{"minute":120}}'
