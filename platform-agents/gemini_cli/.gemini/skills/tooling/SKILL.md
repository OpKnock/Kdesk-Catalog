---
name: "tooling"
description: "Standardizes everyday infra developer tooling: jq/yq data processing, Docker Compose workflows, and task runners."
---

# Tooling

Standardizes everyday infra developer tooling: jq/yq data processing, Docker Compose workflows, and task runners.

## Instructions

# Infrastructure Tooling

Standardize local and CI tooling across the org.

## When to Use

- Parsing API responses or configs in scripts
- Booting full local stacks with one command
- CI pipelines that inspect manifests

## jq for JSON

```bash
jq -r '.items[] | select(.status=="running") | .id' instances.json
curl -s https://api.github.com/repos/opencode/opencode | jq '.stargazers_count'
```

Use `-r` for raw strings, `@csv`/`@tsv` for tables.

## yq for YAML

```bash
yq eval '.services.web.image' docker-compose.yml
yq eval '.services | keys' docker-compose.yml
```

Great for pulling values out of k8s manifests and compose files.

## Compose development loop

```bash
docker compose up -d --build
docker compose ps
docker compose logs -f web
docker compose down -v
```

## Task runner pattern

Use `make` or `task` to encode common commands:

```makefile
up:
	docker compose up -d
lint:
	npx eslint . --max-warnings 0
test:
	npx vitest run
```

```bash
make up make lint
```

## Best practices

- Pin tool versions via mise/asdf in a shared .tool-versions.
- Keep compose files env-driven with .env.example committed.
- Prefer `docker compose run --rm` for one-off jobs.
- Add a CI job that runs every script from the Makefile.

## Testing

```bash
jq empty file.json && echo valid
curl -s <api> | jq -e 'has("data")'
```

Validate JSON/YAML in CI before scripts consume them.

## Capabilities

### data-tools
Process JSON and YAML with jq and yq.

**Commands:**
- `jq '.name, .version' package.json`
- `jq -r '.items[] | select(.status=="running") | .id' instances.json`
- `yq eval '.services.web.image' docker-compose.yml`
- `yq eval '.services | keys' docker-compose.yml`
- `jq '.[] | {id, name} | @csv' data.json`

**Examples:**
- jq -r '.[] | .name' package-lock.json | sort -u | head
- yq eval '.services.redis.ports' docker-compose.yml
- curl -s https://api.github.com/repos/opencode/opencode | jq '.stargazers_count'

### compose
Manage local dev environments with Docker Compose.

**Commands:**
- `docker compose up -d`
- `docker compose ps`
- `docker compose logs -f web`
- `docker compose exec web sh`
- `docker compose down -v`

**Examples:**
- docker compose up -d --build
- docker compose logs --tail=50 api
- docker compose run --rm migrate
