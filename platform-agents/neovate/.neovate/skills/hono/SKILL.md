---
name: "hono"
description: "Scaffold and run Hono web applications targeting edge runtimes: compose middleware chains, define routes, and launch dev servers on Node.js, Bun, Deno, or Cloudflare Workers. Use when working with hono app lifecycle, api or when the user mentions hono app lifecycle, api."
license: "MIT"
compatibility: "Requires bun, npm."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(bun:*) Bash(cd:*) Bash(npm:*)"
---

Scaffold and run Hono web applications targeting edge runtimes: compose middleware chains, define routes, and launch dev servers on Node.js, Bun, Deno, or Cloudflare Workers.

## Agentic Workflow: Read -> Reason -> Act (hono)

You are **Hono** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `hono`
- Domain: Scaffold and run Hono web applications targeting edge runtimes: compose middleware chains, define routes, and launch dev servers on Node.js, Bun, Deno, or Cloudflare Workers.
- **hono-app-lifecycle**: Scaffold, develop, and run Hono applications with the hono CLI and runtime dev servers. — `npm create hono@latest my-app`
- Check `knowledge` and `prerequisites: bun, npm`

### 2. Reason — think for `hono`
- For `hono-app-lifecycle`: Scaffold, develop, and run Hono applications with the hono CLI and runtime dev servers. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `hono` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Cd` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `hono:489e23ce`

# Hono

Build web applications for edge runtimes with Hono.

## What this skill does
48:   
- Scaffolds Hono apps for Node, Bun, Deno, and Workers.
- Structures routing and middleware chains.
49:   - Runs local dev servers with hot reload.
- Deploys to edge platforms.

## When to use

- A small,50:    fast API that must run on edge runtimes.
- Prototyping API endpoints quickly.
- Adding middleware51:    (auth, logging, validation) in a typed framework.

## Real commands

```bash
# Scaffold
npm52:    create hono@latest my-app
cd my-app
npm install

# Pick a template explicitly
npm create hono@latest53:    my-app -- --template cloudflare-workers

# Dev server
npm run dev

# Deploy (template-dependent:54:    workers, vercel, netlify...)
npm run deploy

# Bun runtime
bun run src/index.ts
```

## Basic55:    app

```ts
import { Hono } from 'hono'

const app = new Hono()

app.get('/', (c) => c.text('Hello56:    Hono!'))
app.get('/users/:id', (c) => c.json({ id: c.req.param('id') }))
app.post('/items', async57:    (c) => {
  const body = await c.req.json()
  return c.json({ created: body }, 201)
})

export58:    default app
```

## Middleware

```ts
import { logger } from 'hono/logger'
import { bearerAuth59:    } from 'hono/bearer-auth'

app.use('*', logger())
app.use('/admin/*', bearerAuth({ token: 'secret'60:    }))
```

## Testing

```bash
curl -s http://localhost:3000/ | grep -q "Hello Hono!" && echo61:    OK
```

## Best practices

- Use the built-in logger and bearer auth middleware instead of hand-rolled62:    code.
- Keep handlers small; compose with app.use chains.
- Validate request bodies with a schema63:    library before use.
- Match the runtime (node vs workers) when choosing adapters.

## Example exchange
64:   
```
User: Create a Hono app with a /health route.
Agent: npm create hono@latest my-app && cd my-app65:    && add
       app.get('/health', (c) => c.json({ status: 'ok' }))
```

## Capabilities

### hono-app-lifecycle
Scaffold, develop, and run Hono applications with the hono CLI and runtime dev servers.

**Parameters:**
- `template` (string): Project template: nodejs, bun, cloudflare-workers, deno, vercel, etc.
- `port` (integer): Dev server port.
- `app_name` (string): Project/app name.

**Commands:**
- `npm create hono@latest my-app`
- `cd my-app && npm install`
- `npm run dev`
- `npm run deploy`
- `bun run src/index.ts`

**Examples:**
- npm create hono@latest my-app -- --template cloudflare-workers
- npm run dev -- --port 3001
- npm test

## References
- [Hono Docs](https://hono.dev/docs/)
- [Hono API Reference](https://hono.dev/api/hono)
