---
name: "docker-deployment"
description: "Production Docker deployments: builds multi-stage images, tags and pushes to registries, runs containers with proper restart policies, and rolls back. Use when working with image deploy, api or when the user mentions image deploy, api."
license: "MIT"
compatibility: "Requires docker."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(docker:*)"
---

Production Docker deployments: builds multi-stage images, tags and pushes to registries, runs containers with proper restart policies, and rolls back.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `docker build -t ghcr.io/org/app:v1.2.3 .`
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

# Docker Deployment

## What this skill does

Docker deployment is the art of taking an application from Dockerfile to running container in production: building reproducible images, pushing to a registry, running with correct restart policies, and rolling back safely.

## When to use

- Deploying an application on a single host or small fleet with docker run
- Building images in CI for later release
- Debugging why a production container stopped

## Real commands

```bash
# Build and push
 docker build -t ghcr.io/org/app:v1.2.3 .
 docker login ghcr.io
 docker push ghcr.io/org/app:v1.2.3

# Run in production
 docker run -d --name app --restart unless-stopped -p 8080:8080 -e ENV=prod ghcr.io/org/app:v1.2.3

# Inspect state
 docker inspect app --format '{{json .State}}' | jq
 docker ps -a --filter name=app

# Roll back to the previous tag
 docker rm -f app
 docker run -d --name app --restart unless-stopped -p 8080:8080 ghcr.io/org/app:v1.2.2

# Cleanup
 docker system prune -af --volumes
```

## Multi-stage Dockerfile example

```dockerfile
FROM golang:1.22 AS build
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /bin/app ./cmd/app

FROM alpine:3.20
RUN adduser -D app
COPY --from=build /bin/app /usr/local/bin/app
USER app
EXPOSE 8080
ENTRYPOINT ["/usr/local/bin/app"]
```

## Testing

```bash
# Health check after deploy
curl -sf http://localhost:8080/health && echo OK
# Check container restarts
 docker inspect app --format '{{.RestartCount}}'
```

## Best practices

- Use multi-stage builds; final image should be minimal (distroless or alpine).
- Always run as a non-root user in the container.
- Use `--restart unless-stopped` for services; never `--restart always` with manual runs.
- Tag images with immutable versions, not `latest`, so rollback is deterministic.
- Keep old images for at least one release cycle to enable quick rollback.

## Capabilities

### image-deploy
Build, sign, push, run, and inspect Docker images and containers in deployment pipelines.

**Parameters:**
- `image-tag` (string): Full image reference including registry and tag
- `container-name` (string): Name for the running container
- `port-mapping` (string): host:container port mapping for -p

**Commands:**
- `docker build -t ghcr.io/org/app:v1.2.3 .`
- `docker login ghcr.io`
- `docker push ghcr.io/org/app:v1.2.3`
- `docker run -d --name app --restart unless-stopped -p 8080:8080 -e ENV=prod ghcr.io/org/app:v1.2.3`
- `docker inspect app --format '{{json .State}}' | jq`
- `docker system prune -af --volumes`

**Examples:**
- docker build -t ghcr.io/org/app:v1.2.3 . && docker push ghcr.io/org/app:v1.2.3
- docker run -d --name app --restart unless-stopped -p 8080:8080 ghcr.io/org/app:v1.2.3
- docker tag app:old ghcr.io/org/app:v1.2.2 && docker push ghcr.io/org/app:v1.2.2

## References
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [docker CLI Reference](https://docs.docker.com/reference/cli/docker/)
