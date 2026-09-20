---
name: "fly"
description: "Deploys applications to Fly.io with the flyctl CLI: app creation, scaling machines, volumes, secrets, and wireguard VPN. Use when working with fly deploy, fly ops, cloud or when the user mentions fly deploy, fly ops, cloud."
type: knowledge
triggers: ["fly", "fly-deploy", "fly-ops"]
---

Deploys applications to Fly.io with the flyctl CLI: app creation, scaling machines, volumes, secrets, and wireguard VPN.

## Agentic Workflow: Read -> Reason -> Act (fly)

You are **Fly** (cloud/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — cloud context for `fly`
- Domain: Deploys applications to Fly.io with the flyctl CLI: app creation, scaling machines, volumes, secrets, and wireguard VPN.
- **fly-deploy**: Create apps, launch machines, and deploy. — `fly launch`
- **fly-ops**: Manage machines, volumes, and secrets. — `fly machines list -a myapp`
- Check `knowledge` and `prerequisites: fly`

### 2. Reason — think for `fly`
- For `fly-deploy`: Create apps, launch machines, and deploy. — decide which checks to run
- For `fly-ops`: Manage machines, volumes, and secrets. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `fly` tools
- Tools: `Glob`, `Grep`, `Read`, `Fly` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `fly:f82b1264`

# Fly.io

Deploy apps to edge infrastructure with flyctl.

## When to Use

- Quick global deploys for Dockerized apps
- Stateful services with volumes
- Regional scaling (machines per region)
- Replacement for Heroku-style workflows

## Commands

```bash
# Launch a new app
fly launch
fly launch --name myapp --region lhr --no-deploy

# Deploy
fly deploy
fly deploy --image nginx:alpine

# Status
fly status

# Scale
fly scale count app=3
fly scale count app=5 --max-per-region 2

# Machines
fly machines list -a myapp
fly machines destroy 123abc -a myapp --force

# Volumes
fly volume create data -a myapp --region lhr --size 5
fly volumes list -a myapp

# Secrets
fly secrets set DATABASE_URL=postgres://...
fly secrets list -a myapp

# Shell access
fly ssh console -a myapp
```

## Best Practices

- Set fly.toml app name, internal_port, and min_machines_running
- Use volumes only for stateful data; keep apps stateless
- Manage secrets with fly secrets, never in code
- Test with fly deploy --no-cache for clean builds
- Monitor with fly status and the dashboard metrics
- Pin the primary region; place dependent services together

## Capabilities

### fly-deploy
Create apps, launch machines, and deploy.

**Parameters:**
- `app` (string): Fly app name
- `region` (string): Fly region code

**Commands:**
- `fly launch`
- `fly deploy`
- `fly status`
- `fly apps create myapp`
- `fly scale count app=3`

**Examples:**
- fly launch --name myapp --region lhr --no-deploy
- fly deploy --image nginx:alpine
- fly scale count app=5 --max-per-region 2

### fly-ops
Manage machines, volumes, and secrets.

**Parameters:**
- `machine-id` (string): Machine id
- `secret` (string): KEY=VALUE pair

**Commands:**
- `fly machines list -a myapp`
- `fly volume create data -a myapp --region lhr --size 5`
- `fly secrets set DATABASE_URL=postgres://...`
- `fly secrets list -a myapp`
- `fly ssh console -a myapp`

**Examples:**
- fly machines destroy 123abc -a myapp --force
- fly volumes list -a myapp
- fly secrets set --detach AUTH_TOKEN=abc123

## References
- [Fly.io Docs](https://fly.io/docs/)
- [flyctl Reference](https://fly.io/docs/flyctl/)
