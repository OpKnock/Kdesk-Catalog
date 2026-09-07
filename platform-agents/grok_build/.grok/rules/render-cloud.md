Deploys web services, static sites, and background workers to Render with the CLI and render.yaml infrastructure configs.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm install -g @render/cli`, `render blueprints apply --file render.yaml`
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

Deploy apps on Render.

## When to Use

- Web services from Docker or buildpacks
- Static sites and SPAs
- Background workers and cron jobs
- Managed Postgres and Redis

## render.yaml Example

```yaml
services:
  - type: web
    name: api
    runtime: node
    plan: starter
    buildCommand: npm ci && npm run build
    startCommand: node dist/server.js
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: mydb
          property: connectionString
databases:
  - name: mydb
    plan: basic
```

## Commands

```bash
# Setup
npm install -g @render/cli
render login

# Deploy a specific service
render deploy --service svc_123
render deploy --service svc_123 --commit main

# List and inspect
render services list
render logs --service svc_123

# Blueprints
render blueprints apply --file render.yaml
render blueprints list
render project list
```

## Best Practices

- Define all services in render.yaml for repeatable environments
- Use the database property to wire connection strings automatically
- Set health check paths on every web service
- Deploy previews from PR branches to a separate service
- Stream logs with render logs to debug cold starts
- Promote with blueprints so staging and prod match

## Capabilities

### render-cli
Deploy and manage services on Render.

**Parameters:**
- `service` (string): Service id
- `commit` (string): Commit or branch to deploy

**Commands:**
- `npm install -g @render/cli`
- `render login`
- `render deploy --service demo-service-id`
- `render services list`
- `render logs --service demo-service-id`

**Examples:**
- render deploy --service svc_123 --commit main
- render services list --project prj_abc
- render blueprints apply

### render-infra
Manage render.yaml blueprint infrastructure.

**Parameters:**
- `file` (string): render.yaml path
- `detach` (boolean): Do not wait for apply to finish

**Commands:**
- `render blueprints apply --file render.yaml`
- `render blueprints list`
- `render project list`
- `render env group list`

**Examples:**
- render blueprints apply --file render.yaml --detach
- render blueprints index --file render.yaml

## References
- [Render Docs](https://docs.render.com)
- [Render Blueprint Spec](https://docs.render.com/blueprint-spec)