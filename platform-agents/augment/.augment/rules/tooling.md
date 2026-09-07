---
type: agent_requested
description: "Standardizes everyday infra developer tooling: jq/yq data processing, Docker Compose workflows, and task runners. Use when working with data tools, compose, infrastructure or when the user mentions data tools, compose, infrastructure."
---

Standardizes everyday infra developer tooling: jq/yq data processing, Docker Compose workflows, and task runners.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `jq '.name, .version' package.json`, `docker compose up -d`
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

**Parameters:**
- `filter` (string): jq/yq filter expression
- `input` (string): Input JSON/YAML file
- `output` (string): Output transformation like @csv, @tsv

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

**Parameters:**
- `service` (string): Compose service name
- `detach` (string): Run in background with -d
- `follow` (string): Follow logs with -f

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

## References
- [jq Manual](https://jqlang.github.io/jq/manual/)
- [yq Docs](https://mikefarah.gitbook.io/yq)
- [Docker Compose](https://docs.docker.com/compose/)