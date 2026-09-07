---
name: "vercel"
description: "Deploys frontend and serverless functions with Vercel: CLI deploys, project linking, environment variables, and previews. Use when working with vercel cli, vercel config, cloud or when the user mentions vercel cli, vercel config, cloud."
license: "MIT"
compatibility: "Requires npm, vercel."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "cloud"}
allowed-tools: "Glob Grep Read Bash(npm:*) Bash(vercel:*)"
---

Deploys frontend and serverless functions with Vercel: CLI deploys, project linking, environment variables, and previews.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm install -g vercel`, `vercel env add API_KEY production`
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

# Vercel

Deploy frontend apps and serverless functions.

## When to Use

- Next.js, Vite, and static sites
- Preview deployments for every PR
- Serverless functions and edge middleware
- Global CDN with automatic caching

## Commands

```bash
# Setup
npm install -g vercel
vercel login
vercel link

# Deploy
vercel            # preview
vercel --prod     # production
vercel --prebuilt # use local build output

# Local dev
vercel dev

# Env vars
vercel env add API_KEY production
vercel env add DATABASE_URL preview
vercel env ls
vercel env rm API_KEY production

# Inspect
vercel ls
vercel project ls
```

## vercel.json Example

```json
{
  "builds": [{ "src": "api/**/*.js", "use": "@vercel/node" }],
  "rewrites": [{ "source": "/api/(.*)", "destination": "/api/$1" }]
}
```

## Best Practices

- Let PRs create preview deployments automatically
- Scope env vars to production/preview/development
- Use vercel pull in CI to sync env before builds
- Verify redirects and rewrites locally with vercel dev
- Monitor deployment status with vercel ls
- Pin the CLI version in CI scripts

## Capabilities

### vercel-cli
Build, deploy, and manage Vercel projects.

**Parameters:**
- `prod` (boolean): Deploy to production
- `prebuilt` (boolean): Deploy prebuilt output

**Commands:**
- `npm install -g vercel`
- `vercel login`
- `vercel`
- `vercel --prod`
- `vercel dev`

**Examples:**
- vercel --prod --yes
- vercel deploy --prebuilt
- vercel --prod --name myapp

### vercel-config
Manage environment variables and project settings.

**Parameters:**
- `name` (string): Env var name
- `env` (string): production, preview, development

**Commands:**
- `vercel env add API_KEY production`
- `vercel env ls`
- `vercel env rm API_KEY production`
- `vercel link`
- `vercel ls`

**Examples:**
- vercel env add DATABASE_URL preview
- vercel pull --environment=production
- vercel project ls

## References
- [Vercel Docs](https://vercel.com/docs)
- [Vercel CLI Reference](https://vercel.com/docs/cli)
