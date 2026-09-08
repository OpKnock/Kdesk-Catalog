---
type: agent_requested
description: "Designs gateway routing and policies: route matching, rate limit tiers, JWT validation, and failover before implementation. Use when working with routing design, policy design or when the user mentions routing design, policy design."
---

Designs gateway routing and policies: route matching, rate limit tiers, JWT validation, and failover before implementation.

## Agentic Workflow: Read -> Reason -> Act (api-gateway-routing-design)

You are **Api Gateway Routing Design** (infrastructure) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — infrastructure context for `api-gateway-routing-design`
- Domain: Designs gateway routing and policies: route matching, rate limit tiers, JWT validation, and failover before implementation.
- **routing-design**: Design route matching rules: paths, hosts, headers, and methods — `node -e "const r={paths:['/api/v1/orders'],hosts:['api.example.com'],methods:['G`
- **policy-design**: Design rate limit tiers, quotas, and auth policies — `node -e "const tiers={free:{minute:10},pro:{minute:120},enterprise:{minute:1000}`
- Check `knowledge` and `prerequisites: kong, traefik, aws-cli`

### 2. Reason — think for `api-gateway-routing-design`
- For `routing-design`: Design route matching rules: paths, hosts, headers, and methods — decide which checks to run
- For `policy-design`: Design rate limit tiers, quotas, and auth policies — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-gateway-routing-design` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-gateway-routing-design:50499283`

# API Gateway (Design)

Designs gateway routes and policies before wiring them up.

## When to Use
- Planning gateway rollout
- Defining rate-limit tiers
- Deciding route ownership

## Real Commands

```bash
# Route model
node -e "const r={paths:['/api/v1/orders'],hosts:['api.example.com'],methods:['GET','POST']};console.log(JSON.stringify(r,null,2))"

# Tiers
node -e "const tiers={free:{minute:10},pro:{minute:120},enterprise:{minute:1000}};console.log(JSON.stringify(tiers,null,2))"

# Consumers
curl -s -X POST http://localhost:8001/consumers -H 'Content-Type: application/json' -d '{"username":"acme"}'
curl -s -X POST http://localhost:8001/consumers/acme/plugins -H 'Content-Type: application/json' -d '{"name":"rate-limiting","config":{"minute":120}}'
```

## Design Checklist
- Versioned path prefixes
- Internal vs public route split
- Per-tier quotas and burst allowances

## Testing
Probe each tier's limit and verify 429 responses carry retry headers.

## Best Practices
- Design routes before plugins
- Key limits by consumer, not IP

## Capabilities

### routing-design
Design route matching rules: paths, hosts, headers, and methods

**Parameters:**
- `path` (string): Route path
- `host` (string): Route host

**Commands:**
- `node -e "const r={paths:['/api/v1/orders'],hosts:['api.example.com'],methods:['GET','POST']};console.log(JSON.stringify(r,null,2))"`
- `node -e "console.log('priority: method > header > path > host')"`
- `curl -s -H 'Host: api.example.com' http://localhost:8000/api/v1/orders -o /dev/null -w '%{http_code}'`
- `node -e "const routes=['/api/v1/*','/internal/*','/healthz'];console.log(routes.join('\n'))"`
- `curl -s http://localhost:8000/healthz -o /dev/null -w '%{http_code}'`

**Examples:**
- node -e "const r={paths:['/api/v1/orders'],hosts:['api.example.com'],methods:['GET','POST']};console.log(JSON.stringify(r,null,2))"
- curl -s -H 'Host: api.example.com' http://localhost:8000/api/v1/orders -o /dev/null -w '%{http_code}'
- curl -s http://localhost:8000/healthz -o /dev/null -w '%{http_code}'

### policy-design
Design rate limit tiers, quotas, and auth policies

**Parameters:**
- `consumer` (string): Consumer name
- `tier` (string): Rate limit tier

**Commands:**
- `node -e "const tiers={free:{minute:10},pro:{minute:120},enterprise:{minute:1000}};console.log(JSON.stringify(tiers,null,2))"`
- `node -e "console.log('burst: 2x rate, keyed by consumer id')"`
- `curl -s -X POST http://localhost:8001/consumers -H 'Content-Type: application/json' -d '{"username":"acme"}'`
- `curl -s -X POST http://localhost:8001/consumers/acme/plugins -H 'Content-Type: application/json' -d '{"name":"rate-limiting","config":{"minute":120}}'`
- `curl -s -X POST http://localhost:8001/consumers/acme/key-auth -H 'Content-Type: application/json' -d '{}'`

**Examples:**
- node -e "const tiers={free:{minute:10},pro:{minute:120},enterprise:{minute:1000}};console.log(JSON.stringify(tiers,null,2))"
- curl -s -X POST http://localhost:8001/consumers/acme/plugins -H 'Content-Type: application/json' -d '{"name":"rate-limiting","config":{"minute":120}}'
- curl -s -X POST http://localhost:8001/consumers/acme/key-auth -H 'Content-Type: application/json' -d '{}'

## References
- [Kong Routing](https://docs.konghq.com/gateway/latest/key-concepts/routes/)
- [Rate Limiting Design](https://docs.konghq.com/hub/kong-inc/rate-limiting/)