---
name: "fly-io"
description: "Deploy applications to Fly.io edge infrastructure with flyctl: launch apps, scale machines, manage volumes, and wire secrets."
type: knowledge
triggers: ["fly-io", "flyctl-deploy"]
---

# Fly Io

Deploy applications to Fly.io edge infrastructure with flyctl: launch apps, scale machines, manage volumes, and wire secrets.

## Instructions

# Fly.io

## What this skill does

Fly.io runs containerized apps on micro-VMs distributed across regions. flyctl launches apps, deploys from Dockerfiles, scales machines, attaches volumes, and manages secrets.

## When to use

- Deploying an app close to users in multiple regions
- Attaching persistent volumes to stateful services
- Simple single-command deploys from CI

## Real commands

```bash
# Launch and deploy
fly launch --name myapp --region ams
fly deploy

# Status and logs
fly status
fly logs

# Scale
fly scale count 3 --region ams
fly scale show

# Secrets and volumes
fly secrets set DATABASE_URL=postgres://user:pass@host/db
fly volumes create data --size 10 --region ams
```

## fly.toml example

```toml
app = "myapp"
primary_region = "ams"

[build]
  dockerfile = "Dockerfile"

[mounts]
  source = "data"
  destination = "/data"

[[services]]
  internal_port = 8080
  protocol = "tcp"
  [[services.ports]]
    handlers = ["http"]
    port = 80
```

## Testing

```bash
# Deploy a preview environment
fly deploy --image myapp:preview
fly curl myapp.fly.dev/health
```

## Best practices

- Mount volumes only where state lives; keep app machines stateless.
- Use `fly secrets` for config, not env in fly.toml.
- Pin regions for latency-sensitive workloads.
- Test `fly launch --ha=false` for single-node dev, then enable HA.
- Watch `fly status` machine states before and after deploys.

## Capabilities

### flyctl-deploy
Launch, deploy, scale, and monitor apps on Fly.io.

**Commands:**
- `fly launch --name myapp --region ams`
- `fly deploy`
- `fly status`
- `fly scale count 3 --region ams`
- `fly secrets set DATABASE_URL=postgres://...`
- `fly volumes create data --size 10 --region ams`
- `fly logs`

**Examples:**
- fly launch --name myapp --region ams && fly deploy
- fly scale count 3 --region ams && fly status
- fly secrets set DATABASE_URL=postgres://... && fly deploy
