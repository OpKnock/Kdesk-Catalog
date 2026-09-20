---
trigger: glob
description: "Manages multi-container local development and orchestration with Docker Compose: lifecycle commands, logs, exec, config validation, and cleanup."
globs: ["**/*.r", "**/*.sh", "**/*.sql", "**/*.{yaml,yml}"]
---

# Docker Compose

Manages multi-container local development and orchestration with Docker Compose: lifecycle commands, logs, exec, config validation, and cleanup.

## Instructions

# Docker Compose

## What this skill does

Docker Compose defines multi-container apps declaratively in compose.yaml and provides one-command lifecycle management: up, logs, exec, rebuild, and down.

## When to use

- Local development with several services (web, db, cache, queue)
- Reproducible test environments in CI
- One-command startup for new team members

## Real commands

```bash
# Start everything in detached mode
cd project && docker compose up -d

# Rebuild and start only the web service
 docker compose up -d --build web

# Inspect state and stream logs
docker compose ps
docker compose logs -f web --tail=100

# Run a command inside a service
docker compose exec web sh

# Validate the config without starting anything
docker compose config --quiet
docker compose config --services

# Full teardown including named volumes
docker compose down -v
```

## compose.yaml example

```yaml
services:
  web:
    build: .
    ports: ['8080:8080']
    environment:
      DATABASE_URL: postgres://app:app@db:5432/app
    depends_on:
      db:
        condition: service_healthy
  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: app
    healthcheck:
      test: ['CMD-SHELL', 'pg_isready -U app']
      interval: 5s
    volumes:
      - pgdata:/var/lib/postgresql/data
volumes:
  pgdata:
```

## Testing

```bash
# Wait for healthy dependencies and hit the app
until docker compose ps db | grep -q healthy; do sleep 1; done
curl -s localhost:8080/health | jq
```

## Best practices

- Pin image versions (postgres:16 not postgres:latest) for reproducibility.
- Use healthchecks + `depends_on.condition` instead of sleep hacks.
- Keep secrets out of compose files; use .env with `env_file:`.
- Add `--quiet` config validation to CI.
- Use `docker compose down -v` only in dev; it destroys data volumes.

## Capabilities

### compose-lifecycle
Manage Compose projects: start, stop, rebuild, stream logs, exec into services, and validate config.

**Commands:**
- `docker compose up -d`
- `docker compose up -d --build web`
- `docker compose ps`
- `docker compose logs -f web --tail=100`
- `docker compose exec web sh`
- `docker compose config --services`
- `docker compose down -v`

**Examples:**
- docker compose up -d --build web && docker compose logs -f web
- docker compose config --quiet && docker compose up -d
- docker compose down -v && docker compose up -d --force-recreate
