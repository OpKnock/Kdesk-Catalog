Deploys apps to Railway with the CLI: project linking, deploys, services, variables, and logs.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm install -g @railway/cli`, `railway variables`
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

# Railway

Deploy apps with the Railway CLI.

## When to Use

- Quick deploys from a git repo or local directory
- Auto-provisioned Postgres/Redis plugins
- Environments for staging and production
- Simple zero-config deploys for side projects

## Commands

```bash
# Setup
npm install -g @railway/cli
railway login
railway init

# Deploy
railway up
railway up --detach
railway deploy --detach

# Variables
railway variables
railway variables set DATABASE_URL=postgres://...
railway variables set --env production API_KEY=abc

# Observability
railway logs
railway logs --service api
railway status
railway service

# Tear down
railway down
```

## Best Practices

- Link the project once per machine with railway init
- Use --detach for CI so pipelines do not block on logs
- Store secrets in variables, never in repo files
- Use environments to isolate staging from production
- Watch logs after deploy; they stream with railway up
- Pin the CLI version in CI scripts

## Capabilities

### railway-cli
Link projects and deploy services.

**Parameters:**
- `project` (string): Project name
- `detach` (boolean): Do not stream logs

**Commands:**
- `npm install -g @railway/cli`
- `railway login`
- `railway init`
- `railway up`
- `railway deploy`

**Examples:**
- railway init --name myapp
- railway up --detach
- railway deploy --detach

### railway-ops
Manage variables, services, and logs.

**Parameters:**
- `key` (string): Variable name
- `service` (string): Service name

**Commands:**
- `railway variables`
- `railway variables set DATABASE_URL=postgres://...`
- `railway logs`
- `railway service`
- `railway down`

**Examples:**
- railway variables set --env production API_KEY=abc
- railway logs --service api
- railway status

## References
- [Railway Docs](https://docs.railway.com)
- [Railway CLI Reference](https://docs.railway.com/reference/cli-api)