---
name: "nerdctl"
description: "Runs containers with the Docker-compatible containerd CLI (nerdctl): lifecycle, compose, build, and debug on Kubernetes node runtimes. Use when working with container lifecycle, compose and build, devops or when the user mentions container lifecycle, compose and build, devops."
---

Runs containers with the Docker-compatible containerd CLI (nerdctl): lifecycle, compose, build, and debug on Kubernetes node runtimes.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `nerdctl pull nginx:alpine`, `nerdctl build -t myapp:1.0 .`
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

# nerdctl with containerd

Operate containers on containerd with a Docker-compatible CLI.

## What This Skill Does

- Runs and manages containers (run, ps, exec, logs, rm)
- Builds images with BuildKit
- Runs compose stacks against containerd namespaces
- Pulls/pushes images with lazy-pull (stargz) support
- Provides Docker parity for nodes running containerd (K3s, RKE2, bare)

## When to Use

- Nodes have no Docker daemon, only containerd (common on Kubernetes)
- Debugging pods at runtime level on such nodes
- Local containerd-based dev environments

## Real Commands

```bash
# Lifecycle
nerdctl pull nginx:alpine
nerdctl run -d --name web -p 8080:80 nginx:alpine
nerdctl ps -a
nerdctl exec -it web sh
nerdctl logs -f web
nerdctl rm -f web

# Build and compose
nerdctl build -t myapp:1.0 .
nerdctl compose -f compose.yaml up -d
nerdctl compose -f compose.yaml logs -f
nerdctl compose down

# Maintenance
nerdctl images
nerdctl system df
nerdctl system prune -a
nerdctl namespace list
nerdctl --namespace k8s.io ps   # inspect pods' containers on k8s nodes
```

## Best Practices

- On Kubernetes nodes use `--namespace k8s.io` to see pod containers
- Use `nerdctl compose up` for CRI-less environments (e.g. RKE2 control plane)
- Prefer `nerdctl run --cni` for CNI networking in bare setups
- Use stargz lazy-pulling for cold-start sensitive fleets
- Keep containerd and nerdctl versions matched

## Capabilities

### container-lifecycle
Pull, run, list, exec, and remove containers on containerd.

**Parameters:**
- `name` (string): Container name
- `image` (string): Image reference
- `ports` (string): Port mapping

**Commands:**
- `nerdctl pull nginx:alpine`
- `nerdctl run -d --name web -p 8080:80 nginx:alpine`
- `nerdctl ps -a`
- `nerdctl exec -it web sh`
- `nerdctl logs -f web`
- `nerdctl rm -f web`

**Examples:**
- nerdctl run -d --name web -p 8080:80 nginx:alpine
- nerdctl exec -it web sh
- nerdctl ps -a

### compose-and-build
Build images with BuildKit and run compose stacks via containerd.

**Parameters:**
- `tag` (string): Image tag
- `compose-file` (string): Compose file path

**Commands:**
- `nerdctl build -t myapp:1.0 .`
- `nerdctl compose -f compose.yaml up -d`
- `nerdctl compose -f compose.yaml logs -f`
- `nerdctl compose down`
- `nerdctl images`
- `nerdctl system prune -a`

**Examples:**
- nerdctl build -t myapp:1.0 .
- nerdctl compose -f compose.yaml up -d
- nerdctl images

## References
- [nerdctl GitHub](https://github.com/containerd/nerdctl)
- [containerd](https://containerd.io/docs/)
