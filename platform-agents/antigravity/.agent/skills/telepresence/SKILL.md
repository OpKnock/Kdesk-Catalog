---
name: "telepresence"
description: "Develops Kubernetes services locally with Telepresence: connect to clusters, intercept traffic, and preview services without redeploys."
---

# telepresence

Develops Kubernetes services locally with Telepresence: connect to clusters, intercept traffic, and preview services without redeploys.

## Instructions

# Telepresence Local Development

Develop against a live cluster from your laptop: intercept service traffic to local processes.

## What This Skill Does

- Connects your machine into cluster networking (DNS + routing)
- Intercepts requests to a service and sends them to your local process
- Replaces deployment code without redeploying
- Dumps intercepted env vars for local parity
- Shares preview URLs for review traffic

## When to Use

- Developing microservices that depend on cluster services
- Testing changes against staging data without deploying
- Debugging with local breakpoints on live traffic

## Real Commands

```bash
# Connect
telepresence connect
telepresence connect --namespace app
telepresence status
telepresence version

# Intercept
telepresence intercept web --port 8080:80
telepresence intercept api --port 8080 --env-json env.json
telepresence intercept web --port 8080 --mechanism tcp
telepresence intercept web --preview-url      # shareable preview

# Manage
telepresence list --intercepts
telepresence leave web
telepresence quit
```

## Workflow

1. `telepresence connect`
2. Run your local server on port 8080
3. `telepresence intercept web --port 8080:80`
4. Cluster traffic to `web` now hits your laptop process
5. `telepresence leave web` when done

## Best Practices

- Use intercepts, not connect alone, when possible (precise routing)
- Verify intercepted env parity with --env-json
- Never intercept production without explicit approval and time limits
- Quit cleanly: telepresence quit removes all routes
- Prefer namespace-scoped connects in multi-team clusters

## Capabilities

### cluster-connect
Connect local dev environment to a cluster.

**Commands:**
- `telepresence connect`
- `telepresence status`
- `telepresence list`
- `telepresence quit`
- `telepresence connect --namespace app`
- `telepresence version`

**Examples:**
- telepresence connect
- telepresence status
- telepresence quit

### traffic-interception
Intercept service traffic and route it to the local process.

**Commands:**
- `telepresence intercept web --port 8080:80`
- `telepresence intercept api --port 8080 --env-json env.json`
- `telepresence list --intercepts`
- `telepresence leave web`
- `telepresence intercept api --port 8080 --mechanism tcp`
- `telepresence intercept --preview-url api web`

**Examples:**
- telepresence intercept web --port 8080:80
- telepresence leave web
- telepresence intercept api --port 8080 --env-json env.json
