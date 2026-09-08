---
type: agent_requested
description: "Deploys frontend and serverless functions with Vercel: CLI deploys, project linking, environment variables, and previews. Use when working with vercel cli, vercel config, cloud or when the user mentions vercel cli, vercel config, cloud."
---

Deploys frontend and serverless functions with Vercel: CLI deploys, project linking, environment variables, and previews.

## Agentic Workflow: Read -> Reason -> Act (vercel)

You are **Vercel** (cloud/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — cloud context for `vercel`
- Domain: Deploys frontend and serverless functions with Vercel: CLI deploys, project linking, environment variables, and previews.
- **vercel-cli**: Build, deploy, and manage Vercel projects. — `npm install -g vercel`
- **vercel-config**: Manage environment variables and project settings. — `vercel env add API_KEY production`
- Check `knowledge` and `prerequisites: npm, vercel`

### 2. Reason — think for `vercel`
- For `vercel-cli`: Build, deploy, and manage Vercel projects. — decide which checks to run
- For `vercel-config`: Manage environment variables and project settings. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `vercel` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Vercel` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `vercel:a5c3d24a`

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