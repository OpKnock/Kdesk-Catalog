---
name: "render"
description: "Expert deployment reference covering render.yaml blueprints, CLI handling deploy/logs/secrets, and the platform API that enables service inspection and GitOps workflows. Use when working with render deploy, api or when the user mentions render deploy, api."
license: "MIT"
compatibility: "Requires render. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(render:*)"
---

Expert deployment reference covering render.yaml blueprints, CLI handling deploy/logs/secrets, and the platform API that enables service inspection and GitOps workflows.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `render login`
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

# Render

Expert skill for deploying services to Render.com.

## What this skill does

- Defines services, databases, and cron jobs in a render.yaml blueprint
- Deploys and tails logs with the official render-cli
- Manages environment secrets and inspects services via the API

## When to use

- Shipping a web service or API to Render
- Converting manual dashboard clicks into GitOps blueprint deploys
- Debugging failed deploys from the CLI

## Real commands

```bash
# Authenticate the CLI
render login

# Deploy the latest commit of a service
render deploy srv-abc123

# Stream logs
render logs srv-abc123 --tail

# List environment secrets
render secret list srv-abc123

# Inspect services via the API
curl -s https://api.render.com/v1/services -H "Authorization: Bearer $RENDER_API_KEY" | jq -r '.[].serviceDetails.url'
```

## render.yaml blueprint

```yaml
services:
  - type: web
    name: api
    runtime: node
    plan: starter
    region: oregon
    buildCommand: npm ci && npm run build
    startCommand: node dist/index.js
    healthCheckPath: /healthz
     envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: db
          property: connectionString
databases:
  - name: db
    plan: starter
    databaseName: app
```

## Testing a deploy

```bash
curl -sf https://api.onrender.com/healthz && echo healthy
render logs srv-abc123 --tail
```

## Best practices

- Keep the startCommand minimal; Render restarts on health check failure
- Store secrets as env vars, never in the blueprint
- Merge the blueprint via Git to enable automatic deploys

## Capabilities

### render-deploy
Deploy and manage Render.com services with blueprint and CLI

**Parameters:**
- `service_id` (string): Render service identifier like srv-abc123
- `region` (string): Region in render.yaml, e.g. oregon or frankfurt
- `plan` (string): Instance plan, e.g. starter or pro

**Commands:**
- `render login`
- `render deploy srv-abc123`
- `render logs srv-abc123 --tail`
- `render secret list srv-abc123`
- `curl -s https://api.render.com/v1/services -H "Authorization: Bearer $RENDER_API_KEY" | jq '.[0].name'`

**Examples:**
- render deploy srv-abc123
- render logs srv-abc123 --tail
- curl -s https://api.render.com/v1/services -H "Authorization: Bearer $RENDER_API_KEY" | jq -r '.[].serviceDetails.url'

## References
- [Render Blueprint spec](https://render.com/docs/blueprint-spec)
- [render-cli repository](https://github.com/render-oss/render-cli)
