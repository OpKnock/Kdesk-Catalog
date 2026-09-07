---
trigger: glob
description: "Implements API versioning in Express: URL path versioning, version routing, versioned controllers, and default version behavior. Use when working with url versioning, version router or when the user mentions url versioning, version router."
globs: ["**/*.r", "**/*.sh"]
---

Implements API versioning in Express: URL path versioning, version routing, versioned controllers, and default version behavior.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `node -e "const express=require('express'); const app=express`, `node -e "const fs=require('fs'); console.log(fs.existsSync('`
- Check `knowledge` references and prerequisites before proceeding

### 2. Reason
Analyze and plan:
- Compare current state vs desired state (drift, checksums, policy)
- Evaluate trust, compatibility, and risk: use `kdesk trust` and `kdesk doctor` patterns
- Decide: which capabilities/tools are needed, which can be skipped

### 3. Act
Execute with guards:
- Run only `allowed-tools` (see frontmatter); use `safe_path` for writes
- Prefer `Bash` with explicit binaries (`curl`, `kubectl`, `kdesk`) over generic shell
- Record evidence: file paths, checksums, and tool outputs for verification

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
