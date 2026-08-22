---
name: "vercel-edge"
description: "Deploys and manages Vercel edge functions using the Vercel CLI. Handles authentication, local development with vercel dev, environment variables per environment, preview and production deployments, and rollbacks."
---

# Vercel Edge

Deploys and manages Vercel edge functions using the Vercel CLI. Handles authentication, local development with vercel dev, environment variables per environment, preview and production deployments, and rollbacks.

## Instructions

# Vercel Edge

## What this skill does

Manage Vercel deployments for APIs and edge functions using the Vercel CLI. Covers authentication, local development with `vercel dev`, environment variables, preview vs production deploys, and rollbacks.

## When to use

- Deploying a Next.js API or standalone edge function
- Managing per-environment secrets
- Debugging preview vs production differences

## Real commands

```bash
# Authenticate and link project
vercel login
vercel link

# Local development with functions and env
vercel dev

# Preview deployment (default)
vercel deploy

# Production deployment
vercel deploy --prod

# Deploy without rebuild (CI scenario)
vercel deploy --prebuilt --prod

# Environment variables
vercel env add DATABASE_URL production
vercel env pull

# List deployments and rollback
vercel ls
vercel rollback <deployment-url>
```

## Edge function example (api/hello.ts)

```ts
export const config = { runtime: 'edge' };
export default function handler(req: Request) {
  return new Response(JSON.stringify({ hello: 'edge' }), {
    headers: { 'content-type': 'application/json' },
  });
}
```

## Best practices

- Always test with `vercel dev` before deploying
- Scope env vars per environment (development/preview/production)
- Use `--prebuilt` in CI to keep builds reproducible
- Roll back immediately if production errors spike after deploy

## Testing

```bash
vercel dev &
curl http://localhost:3000/api/hello
```

## Capabilities

### deploy-vercel
Deploy projects and manage edge functions

**Commands:**
- `vercel login`
- `vercel dev`
- `vercel deploy --prod`
- `vercel env add DATABASE_URL production`
- `vercel ls`

**Examples:**
- vercel deploy --prebuilt
- vercel env pull
- vercel rollback
