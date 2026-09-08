---
name: "railway"
description: "Deploy to Railway: login, init, link, deploy, variables, logs and project management with the railway CLI. Use when working with railway deployments, api or when the user mentions railway deployments, api."
type: knowledge
triggers: ["railway", "railway-deployments"]
---

Deploy to Railway: login, init, link, deploy, variables, logs and project management with the railway CLI.

## Agentic Workflow: Read -> Reason -> Act (railway)

You are **Railway** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `railway`
- Domain: Deploy to Railway: login, init, link, deploy, variables, logs and project management with the railway CLI.
- **railway-deployments**: Deploy applications to Railway, manage environment variables and inspect deployments. — `railway login`
- Check `knowledge` and `prerequisites: railway`

### 2. Reason — think for `railway`
- For `railway-deployments`: Deploy applications to Railway, manage environment variables and inspect deployments. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `railway` tools
- Tools: `Glob`, `Grep`, `Read`, `Railway` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `railway:10913cb4`

# Railway

Railway deploys apps with zero config: push code, it runs.

## What this skill does

- Logs in and links projects
- Deploys from the current directory
- Manages variables and runs commands in the environment

## When to use

- Heroku-style deploys without the lock-in
- Preview environments per PR

## Real commands

```bash
# Auth
railway login
railway init
railway link

# Deploy
railway up
railway deploy

# Variables
railway variables
railway variables --set FOO=bar
railway variables --delete FOO

# Run in project env
railway run npm run migrate
railway run python manage.py migrate

# Logs
railway logs
railway logs --deployment
```

## Best practices

- Keep secrets in variables, never in git
- Use railway up for quick deploys, railway deploy for pinned environments
- Run migrations via railway run before releases

## Capabilities

### railway-deployments
Deploy applications to Railway, manage environment variables and inspect deployments.

**Parameters:**
- `project` (string): Railway project name
- `environment` (string): Deploy environment (production/preview)
- `variable` (string): KEY=VALUE to set

**Commands:**
- `railway login`
- `railway init`
- `railway up`
- `railway deploy`
- `railway variables`

**Examples:**
- railway up
- railway variables --set FOO=bar
- railway run npm run migrate

## References
- [Railway Docs](https://docs.railway.com/)
- [Railway CLI GitHub](https://github.com/railwayapp/cli)
