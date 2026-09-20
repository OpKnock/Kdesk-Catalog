---
name: "api-version-engineer"
description: "Implements API versioning in Express: URL path versioning, version routing, versioned controllers, and default version behavior. Use when working with url versioning, version router or when the user mentions url versioning, version router."
globs: ["**/*.r", "**/*.sh"]
alwaysApply: false
---

Implements API versioning in Express: URL path versioning, version routing, versioned controllers, and default version behavior.

## Agentic Workflow: Read -> Reason -> Act (api-version-engineer)

You are **api-version-engineer** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `api-version-engineer`
- Domain: Implements API versioning in Express: URL path versioning, version routing, versioned controllers, and default version behavior.
- **url-versioning**: Route requests by versioned URL paths — `node -e "const express=require('express'); const app=express(); app.use('/v1', r`
- **version-router**: Structure versioned routers and shared middleware — `node -e "const fs=require('fs'); console.log(fs.existsSync('routes/v2/users.js')`
- Check `knowledge` and `prerequisites: node.js, python, openapi`

### 2. Reason — think for `api-version-engineer`
- For `url-versioning`: Route requests by versioned URL paths — decide which checks to run
- For `version-router`: Structure versioned routers and shared middleware — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-version-engineer` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-version-engineer:7787f0a3`

# API Version Engineer

URL-based API versioning.

## What This Skill Does
- Mounts versioned routers at /v1, /v2 paths
- Keeps versions in isolated modules
- Controls default version behavior

## When to Use
- Public APIs with external consumers
- Adding breaking changes safely
- Supporting multiple client cohorts

## Real Commands

```bash
node -e "const express=require('express'); const app=express(); app.use('/v1', require('./v1Routes')); app.use('/v2', require('./v2Routes')); app.listen(3000)"
curl -s http://localhost:3000/v1/users | jq '.apiVersion'
curl -s http://localhost:3000/v2/users | jq '.apiVersion'
```

## Structure

```
routes/
  v1/users.js
  v2/users.js
```

## Testing
- Test each version independently
- Verify default version behavior
- Assert unknown versions 404 cleanly

## Best Practices
- Keep version routers thin
- Share only stable middleware
- Document sunset dates per version

## Capabilities

### url-versioning
Route requests by versioned URL paths

**Parameters:**
- `version` (string): Version prefix like v1 or v2
- `router` (string): Router module path
- `default-version` (string): Version served at the bare path

**Commands:**
- `node -e "const express=require('express'); const app=express(); app.use('/v1', require('./v1Routes')); app.use('/v2', require('./v2Routes')); app.listen(3000)"`
- `curl -s http://localhost:3000/v1/users | jq '.apiVersion'`
- `curl -s http://localhost:3000/v2/users | jq '.apiVersion'`
- `curl -s http://localhost:3000/users -o /dev/null -w '%{http_code}\n'`

**Examples:**
- app.use('/v1', v1Routes) mounts versioned routers
- curl /v2/users hits the current version
- Unversioned paths can 404 or default

### version-router
Structure versioned routers and shared middleware

**Commands:**
- `node -e "const fs=require('fs'); console.log(fs.existsSync('routes/v2/users.js'))"`
- `curl -s -o /dev/null -w '%{http_code}\n' http://localhost:3000/v9/users`
- `curl -s http://localhost:3000/v1/users | jq '.count'`

**Examples:**
- -cli --help
- -api --help

## References
- [Express Routing](https://expressjs.com/en/guide/routing.html)
- [Stripe API Versioning Guide](https://docs.stripe.com/api/versioning)