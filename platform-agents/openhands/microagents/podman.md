---
name: "podman"
description: "Runs daemonless containers with Podman: build, run, pods, quadlets, compose, and Kubernetes YAML generation without root."
type: knowledge
triggers: ["podman", "container-lifecycle", "pods-and-kubernetes"]
---

# podman

Runs daemonless containers with Podman: build, run, pods, quadlets, compose, and Kubernetes YAML generation without root.

## Instructions

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
