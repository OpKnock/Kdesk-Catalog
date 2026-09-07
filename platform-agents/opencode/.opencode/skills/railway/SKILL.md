---
name: "railway"
description: "Deploy to Railway: login, init, link, deploy, variables, logs and project management with the railway CLI. Use when working with railway deployments, api or when the user mentions railway deployments, api."
---

Deploy to Railway: login, init, link, deploy, variables, logs and project management with the railway CLI.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `railway login`
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
