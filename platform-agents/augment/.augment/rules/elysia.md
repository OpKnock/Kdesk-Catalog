---
type: agent_requested
description: "Build TypeScript APIs with the Elysia framework (Bun): scaffold endpoints, run the dev server, and test routes. Use when working with elysia development, api or when the user mentions elysia development, api."
---

Build TypeScript APIs with the Elysia framework (Bun): scaffold endpoints, run the dev server, and test routes.

## Agentic Workflow: Read -> Reason -> Act (elysia)

You are **Elysia** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `elysia`
- Domain: Build TypeScript APIs with the Elysia framework (Bun): scaffold endpoints, run the dev server, and test routes.
- **elysia-development**: Scaffold, run, and test Elysia Bun apps with the bun runtime. — `bun create elysia app`
- Check `knowledge` and `prerequisites: bun`

### 2. Reason — think for `elysia`
- For `elysia-development`: Scaffold, run, and test Elysia Bun apps with the bun runtime. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `elysia` tools
- Tools: `Glob`, `Grep`, `Read`, `Bun` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `elysia:986b7a6a`

# Elysia

## What this skill does

Elysia is a TypeScript-first web framework built for Bun, with end-to-end type safety inferred from route handlers. It has a built-in dev server, Bun-native runtime, and a large plugin ecosystem.

## When to use

- Starting a new TypeScript API with Bun as the runtime
- Migrating Express/Fastify services to Bun for speed
- Prototyping a typed API quickly

## Real commands

```bash
# Scaffold
bun create elysia app
cd app

# Dev server with watch
bun run --watch src/index.ts

# Install plugins
bun add @elysiajs/cors @elysiajs/jwt

# Tests and build
bun test
bun build src/index.ts --target=bun --outdir dist
```

## Minimal app example

```typescript
import { Elysia, t } from 'elysia'

const app = new Elysia()
  .get('/', () => 'Hello Elysia')
  .get('/hello/:name', ({ params }) => `Hello ${params.name}`)
  .post('/orders', ({ body }) => ({ created: body.id }), {
    body: t.Object({ id: t.String() })
  })
  .listen(3000)

console.log(`Running at ${app.server?.hostname}:${app.server?.port}`)
```

## Testing

```bash
# Inline tests with bun:test
bun test src/app.test.ts
# Manual check
curl -s localhost:3000/hello/world | jq
```

## Best practices

- Let Elysia infer types; don't hand-write duplicate interfaces.
- Use the `t` schema validator for request bodies to get validation + types for free.
- Keep plugins in `@elysiajs/*` scope where possible.
- For production, build with `bun build --target=bun` and run the compiled file.

## Capabilities

### elysia-development
Scaffold, run, and test Elysia Bun apps with the bun runtime.

**Parameters:**
- `port` (integer): Port Elysia listens on (default 3000)
- `watch` (boolean): Run the dev server with hot reload
- `target` (string): Build target for bun build

**Commands:**
- `bun create elysia app`
- `bun add elysia`
- `bun run --watch src/index.ts`
- `bun test`
- `bun build src/index.ts --target=bun --outdir dist`

**Examples:**
- bun create elysia app && cd app && bun run --watch src/index.ts
- bun add elysia @elysiajs/cors @elysiajs/jwt
- curl -s localhost:3000/hello/name | jq

## References
- [Elysia Documentation](https://elysiajs.com/)