---
trigger: glob
description: "Develops Kubernetes services locally with Telepresence: connect to clusters, intercept traffic, and preview services without redeploys. Use when working with cluster connect, traffic interception, devops or when the user mentions cluster connect, traffic interception, devops."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

Develops Kubernetes services locally with Telepresence: connect to clusters, intercept traffic, and preview services without redeploys.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `telepresence connect`, `telepresence intercept web --port 8080:80`
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

**Parameters:**
- `namespace` (string): Namespace to connect into
- `context` (string): Kube context to connect into

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

**Parameters:**
- `service` (string): Service to intercept
- `port` (string): Local:remote port mapping
- `env-json` (string): File to dump intercepted env vars

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

## References
- [Telepresence Documentation](https://www.telepresence.io/docs)
- [Telepresence GitHub](https://github.com/telepresenceio/telepresence)
