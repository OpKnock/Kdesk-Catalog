---
name: "railway-cloud"
description: "Deploys apps to Railway with the CLI: project linking, deploys, services, variables, and logs."
---

# Railway

Deploys apps to Railway with the CLI: project linking, deploys, services, variables, and logs.

## Instructions

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
