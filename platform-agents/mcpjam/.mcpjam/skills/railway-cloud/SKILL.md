---
name: "railway-cloud"
description: "Deploys apps to Railway with the CLI: project linking, deploys, services, variables, and logs. Use when working with railway cli, railway ops, cloud or when the user mentions railway cli, railway ops, cloud."
license: "MIT"
compatibility: "Requires npm, railway."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "cloud"}
allowed-tools: "Glob Grep Read Bash(npm:*) Bash(railway:*)"
---

Deploys apps to Railway with the CLI: project linking, deploys, services, variables, and logs.

## Agentic Workflow: Read -> Reason -> Act (railway-cloud)

You are **Railway** (cloud/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — cloud context for `railway-cloud`
- Domain: Deploys apps to Railway with the CLI: project linking, deploys, services, variables, and logs.
- **railway-cli**: Link projects and deploy services. — `npm install -g @railway/cli`
- **railway-ops**: Manage variables, services, and logs. — `railway variables`
- Check `knowledge` and `prerequisites: npm, railway`

### 2. Reason — think for `railway-cloud`
- For `railway-cli`: Link projects and deploy services. — decide which checks to run
- For `railway-ops`: Manage variables, services, and logs. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `railway-cloud` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Railway` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `railway-cloud:0e6b3903`

# Railway

Deploy apps with the Railway CLI.

## When to Use

- Quick deploys from a git repo or local directory
- Auto-provisioned Postgres/Redis plugins
- Environments for staging and production
- Simple zero-config deploys for side projects

## Commands

```bash
# Setup
npm install -g @railway/cli
railway login
railway init

# Deploy
railway up
railway up --detach
railway deploy --detach

# Variables
railway variables
railway variables set DATABASE_URL=postgres://...
railway variables set --env production API_KEY=abc

# Observability
railway logs
railway logs --service api
railway status
railway service

# Tear down
railway down
```

## Best Practices

- Link the project once per machine with railway init
- Use --detach for CI so pipelines do not block on logs
- Store secrets in variables, never in repo files
- Use environments to isolate staging from production
- Watch logs after deploy; they stream with railway up
- Pin the CLI version in CI scripts

## Capabilities

### railway-cli
Link projects and deploy services.

**Parameters:**
- `project` (string): Project name
- `detach` (boolean): Do not stream logs

**Commands:**
- `npm install -g @railway/cli`
- `railway login`
- `railway init`
- `railway up`
- `railway deploy`

**Examples:**
- railway init --name myapp
- railway up --detach
- railway deploy --detach

### railway-ops
Manage variables, services, and logs.

**Parameters:**
- `key` (string): Variable name
- `service` (string): Service name

**Commands:**
- `railway variables`
- `railway variables set DATABASE_URL=postgres://...`
- `railway logs`
- `railway service`
- `railway down`

**Examples:**
- railway variables set --env production API_KEY=abc
- railway logs --service api
- railway status

## References
- [Railway Docs](https://docs.railway.com)
- [Railway CLI Reference](https://docs.railway.com/reference/cli-api)
