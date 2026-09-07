---
name: "podman"
description: "Runs daemonless containers with Podman: build, run, pods, quadlets, compose, and Kubernetes YAML generation without root. Use when working with container lifecycle, pods and kubernetes, devops or when the user mentions container lifecycle, pods and kubernetes, devops."
license: "MIT"
compatibility: "Requires podman."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "devops"}
allowed-tools: "Glob Grep Read Bash(podman:*)"
---

Runs daemonless containers with Podman: build, run, pods, quadlets, compose, and Kubernetes YAML generation without root.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `podman pull nginx:alpine`, `podman pod create --name webpod -p 8080:80`
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

# Podman Containers

Run containers daemonlessly with Podman — Docker-compatible but rootless by default.

## What This Skill Does

- Runs containers/pods without a daemon (fork-exec model)
- Builds images with buildah-compatible frontend
- Generates Kubernetes YAML from running pods
- Runs compose files via podman-compose or podman play
- Manages macOS/Windows VMs with podman machine

## When to Use

- Rootless container workflows on Linux workstations/servers
- RHEL/Fedora environments where Docker is replaced
- Generating Kubernetes manifests from running containers

## Real Commands

```bash
# Lifecycle
podman pull nginx:alpine
podman run -d --name web -p 8080:80 nginx:alpine
podman ps -a
podman exec -it web sh
podman logs -f web
podman rm -f web

# Build and images
podman build -t myapp:1.0 .
podman images
podman push ghcr.io/myapp:1.0

# Pods and Kubernetes
podman pod create --name webpod -p 8080:80
podman run -d --pod webpod nginx
podman generate kube webpod > webpod.yaml
podman play kube webpod.yaml

# Compose + machine
podman compose -f compose.yaml up -d
podman machine init --cpus 4 --memory 4096
podman machine start
```

## Best Practices

- Run rootless unless bind-mounting privileged devices
- Use pods for sidecar groupings that must share localhost
- Prefer podman play kube to standardize on Kubernetes YAML
- Add `--userns=keep-id` for clean bind-mount permissions
- For Docker parity, alias docker=podman and test with docker compose v1 projects

## Capabilities

### container-lifecycle
Run and manage rootless containers with podman.

**Parameters:**
- `name` (string): Container name
- `image` (string): Image reference
- `ports` (string): Port mapping

**Commands:**
- `podman pull nginx:alpine`
- `podman run -d --name web -p 8080:80 nginx:alpine`
- `podman ps -a`
- `podman exec -it web sh`
- `podman logs -f web`
- `podman rm -f web`

**Examples:**
- podman run -d --name web -p 8080:80 nginx:alpine
- podman ps -a
- podman logs -f web

### pods-and-kubernetes
Create pods, run compose stacks, and generate Kubernetes YAML.

**Parameters:**
- `pod` (string): Pod name
- `yaml` (string): Kubernetes YAML file

**Commands:**
- `podman pod create --name webpod -p 8080:80`
- `podman run -d --pod webpod nginx`
- `podman generate kube webpod > webpod.yaml`
- `podman play kube webpod.yaml`
- `podman compose -f compose.yaml up -d`
- `podman machine init --cpus 4 --memory 4096`

**Examples:**
- podman pod create --name webpod -p 8080:80
- podman generate kube webpod > webpod.yaml
- podman play kube webpod.yaml

## References
- [Podman Documentation](https://docs.podman.io/)
- [Podman Machine](https://docs.podman.io/en/latest/markdown/podman-machine.1.html)
- [Podman Compose](https://github.com/containers/podman-compose)
