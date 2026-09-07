---
name: "doppler"
description: "Centralizes environment variables and secrets across projects and environments (dev/staging/prod) with Doppler CLI, injecting into processes, CI, and platform sync. Use when working with secrets management, api or when the user mentions secrets management, api."
license: "MIT"
compatibility: "Requires doppler."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(doppler:*)"
---

Centralizes environment variables and secrets across projects and environments (dev/staging/prod) with Doppler CLI, injecting into processes, CI, and platform sync.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `doppler setup`
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

# Doppler

## What this skill does

Doppler centralizes environment variables and secrets across projects and environments (dev/staging/prod). The CLI fetches secrets from the cloud and injects them into processes, CI, or syncs them to platforms like Vercel, Docker, and AWS.

## When to use

- Replacing scattered .env files with a single source of truth
- Onboarding a teammate without sharing credentials in chat
- Injecting secrets into CI jobs or local `npm start`/`docker compose` runs

## Real commands

```bash
# First-time setup (opens browser for auth, selects project+config)
doppler setup

# Get, set, and delete secrets
doppler secrets get DOPPLER_TOKEN
doppler secrets set API_KEY=abc123 --config dev
doppler secrets delete API_KEY --config prod

# Run a command with secrets injected
doppler run -- npm start
doppler run --config dev -- npm test

# Export secrets to a file or stdout
doppler secrets download --format=env --no-file > .env.doppler
doppler secrets download --format=json --no-file | jq .API_KEY
```

## CI usage

```yaml
# GitHub Actions
- name: Setup Doppler
  uses: dopplerhq/action@v3
  with:
    command: run -- npm test
- name: Inject into docker
  run: doppler run -- docker compose up -d
```

## Testing

```bash
# Verify a value exists in prod without printing secrets
doppler secrets get API_KEY --config prod --plain | wc -c
```

## Best practices

- Never commit `.env` or `DOPPLER_TOKEN`; use `doppler setup` on each machine.
- Rotate secrets with `doppler secrets set` + `--config` per environment, not one giant env.
- Use `--no-file` to avoid accidental .env writes in repos.
- Set up Doppler CI secrets sync once instead of hardcoding values in pipelines.
- Scope secret names by environment (DEV_DB_URL vs PROD_DB_URL) only when needed.

## Capabilities

### secrets-management
Manage Doppler projects, configs, and secrets from the CLI; run processes with injected environment variables.

**Parameters:**
- `project` (string): Doppler project name
- `config` (string): Environment config: dev, staging, prod
- `secret-key` (string): Name of the secret to get, set, or delete

**Commands:**
- `doppler setup`
- `doppler secrets get DOPPLER_TOKEN`
- `doppler secrets set API_KEY=abc123 --config dev`
- `doppler run -- npm start`
- `doppler secrets download --format=env --no-file > .env.doppler`
- `doppler secrets delete API_KEY --config prod`
- `doppler projects list`

**Examples:**
- doppler setup && doppler secrets get DOPPLER_TOKEN
- doppler run --config dev -- npm test
- doppler secrets download --format=env --no-file | grep API_KEY

## References
- [Doppler CLI Reference](https://docs.doppler.com/docs/cli)
