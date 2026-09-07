---
applyTo: "**/*.json **/*.r **/*.sh **/Dockerfile*"
---

Builds, runs, and manages containers and images with the docker CLI: images, volumes, networks, and container lifecycle.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `docker run -d --name web -p 8080:80 nginx:1.26`, `docker build -t myapp:1.0 .`
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

# Docker CLI Operations

Build, run, and troubleshoot containers with the docker command line.

## What This Skill Does

- Runs containers with ports, volumes, env, and resource limits
- Builds efficient images with proper layering
- Manages images, volumes, and networks
- Inspects container state and logs for debugging
- Cleans up orphaned resources

## When to Use

- Any container build/run/debug task
- Image optimization and registry pushes
- Disk cleanup on build machines

## Real Commands

```bash
# Run and manage containers
docker run -d --name web -p 8080:80 -e APP_ENV=prod --restart unless-stopped nginx:1.26
docker ps -a
docker exec -it web bash
docker logs --tail 100 web
docker inspect web | jq '.[0].State'
docker stop web && docker rm web

# Images
docker build -t myapp:1.0 .
docker images
docker pull node:20-alpine
docker push ghcr.io/myapp:1.0

# Storage and networking
docker volume create pgdata
docker network create backend
docker run --network backend --volume pgdata:/data postgres:16

# Cleanup
docker system df
docker image prune -a
docker volume prune --filter label=tmp
```

## Efficient Dockerfile

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY . .
ENV NODE_ENV=production
EXPOSE 3000
CMD ["node", "server.js"]
```

## Best Practices

- Combine RUN commands to reduce layers; copy deps before source for cache hits
- Run as non-root; add HEALTHCHECK to images
- Pin base image digests for supply chain safety
- Prefer named volumes over bind mounts for data
- Prune regularly: `docker system prune -af` on CI runners

## Capabilities

### container-lifecycle
Run, stop, exec into, and remove containers with full flag control.

**Parameters:**
- `name` (string): Container name
- `ports` (string): Port mapping, e.g. 8080:80
- `image` (string): Image reference

**Commands:**
- `docker run -d --name web -p 8080:80 nginx:1.26`
- `docker ps -a`
- `docker stop web && docker rm web`
- `docker exec -it web bash`
- `docker logs --tail 100 web`
- `docker inspect web`

**Examples:**
- docker run -d --name web -p 8080:80 nginx:1.26
- docker exec -it web bash
- docker logs --tail 100 web

### images-and-storage
Build images, manage image lifecycle, and work with volumes and networks.

**Parameters:**
- `tag` (string): Image tag, e.g. myapp:1.0
- `path` (string): Build context path

**Commands:**
- `docker build -t myapp:1.0 .`
- `docker images`
- `docker pull node:20-alpine`
- `docker push ghcr.io/myapp:1.0`
- `docker volume create pgdata`
- `docker network create backend`
- `docker system df`

**Examples:**
- docker build -t myapp:1.0 .
- docker volume create pgdata && docker run -v pgdata:/data postgres
- docker system df

## References
- [Docker Engine CLI Reference](https://docs.docker.com/engine/reference/commandline/docker/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Docker Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
