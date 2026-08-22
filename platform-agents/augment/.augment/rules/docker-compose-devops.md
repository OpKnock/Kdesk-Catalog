---
type: agent_requested
description: "Authors and operates multi-container applications with Docker Compose: services, networks, volumes, healthchecks, and profiles."
---

# docker-compose-devops

Authors and operates multi-container applications with Docker Compose: services, networks, volumes, healthchecks, and profiles.

## Instructions

# Docker Compose Applications

Run local dev environments and single-host multi-container apps with compose.yaml.

## What This Skill Does

- Writes service definitions with images, builds, env, volumes, and healthchecks
- Manages the full lifecycle: up, build, restart, down
- Interacts with running services: logs, exec, top
- Validates compose files before deployment
- Uses profiles and overlays for dev/staging/prod variants

## When to Use

- Local development with DB + cache + API sidecars
- CI service containers
- Small single-host production stacks

## Real Commands

```bash
# Lifecycle
docker compose up -d
docker compose up -d --build --force-recreate
docker compose down -v            # remove volumes too
docker compose restart api
docker compose stop

# Interact
docker compose ps
docker compose logs -f api
docker compose exec api sh
docker compose top
docker compose events

# Validate
docker compose config
docker compose config --services
docker compose config --quiet     # exit code only
```

## Sample compose.yaml

```yaml
services:
  api:
    build: ./api
    ports: ["8080:8080"]
    environment:
      DB_URL: postgres://db:5432/app
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
  db:
    image: postgres:16
    volumes: [pgdata:/var/lib/postgresql/data]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app"]
volumes:
  pgdata:
```

## Best Practices

- Always pin image tags; avoid `latest` in compose files
- Use healthchecks with `depends_on.condition` instead of restart loops
- Keep secrets via env_file or Docker secrets, not inline env
- Use profiles (`profiles: ["debug"]`) for optional services
- Test `docker compose config --quiet` in CI to fail invalid files early

## Capabilities

### compose-lifecycle
Build, start, stop, and tear down multi-service stacks defined in compose.yaml.

**Commands:**
- `docker compose up -d`
- `docker compose up --build`
- `docker compose down`
- `docker compose down -v`
- `docker compose restart api`
- `docker compose stop`

**Examples:**
- docker compose up -d --build
- docker compose down -v
- docker compose restart api

### inspect-and-interact
Tail logs, exec into services, and validate the compose file.

**Commands:**
- `docker compose logs -f api`
- `docker compose ps`
- `docker compose exec api sh`
- `docker compose config`
- `docker compose top`
- `docker compose events`

**Examples:**
- docker compose logs -f api
- docker compose exec api sh -c 'npm test'
- docker compose config --services