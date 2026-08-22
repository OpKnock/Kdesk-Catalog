---
type: agent_requested
description: "Builds, runs, and manages containers and images with the docker CLI: images, volumes, networks, and container lifecycle."
---

# docker

Builds, runs, and manages containers and images with the docker CLI: images, volumes, networks, and container lifecycle.

## Instructions

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