---
trigger: glob
description: "Priority-aware rate limiting: separate limits for high/low-priority clients with Kong plugins and nginx maps. Use when working with priority rate limiting, api or when the user mentions priority rate limiting, api."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

Priority-aware rate limiting: separate limits for high/low-priority clients with Kong plugins and nginx maps.

## Agentic Workflow: Read -> Reason -> Act (priority-rate-limiting)

You are **Priority Rate Limiting** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `priority-rate-limiting`
- Domain: Priority-aware rate limiting: separate limits for high/low-priority clients with Kong plugins and nginx maps.
- **priority-rate-limiting**: Enforce different rate limits per priority tier using Kong rate-limiting plugins and nginx map-based — `curl -X POST http://localhost:8001/plugins -H "Content-Type: application/json" -`
- Check `knowledge` references before acting

### 2. Reason — think for `priority-rate-limiting`
- For `priority-rate-limiting`: Enforce different rate limits per priority tier using Kong rate-limiting plugins and nginx map-based configs. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `priority-rate-limiting` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `priority-rate-limiting:544e0521`

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

**Parameters:**
- `priority_header` (string): Header marking client priority
- `low_limit` (integer): Rate limit for low priority
- `high_limit` (integer): Rate limit for high priority

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

## References
- [Kong rate-limiting plugin](https://docs.konghq.com/hub/kong-inc/rate-limiting/)
- [nginx limit_req module](https://nginx.org/en/docs/http/ngx_http_limit_req_module.html)
