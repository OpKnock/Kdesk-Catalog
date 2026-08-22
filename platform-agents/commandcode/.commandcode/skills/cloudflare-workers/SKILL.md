---
name: "cloudflare-workers"
description: "Build and deploy edge APIs with Cloudflare Workers using wrangler: init, dev, deploy, secrets, and tail."
---

# Cloudflare Workers

Build and deploy edge APIs with Cloudflare Workers using wrangler: init, dev, deploy, secrets, and tail.

## Instructions

# Cloudflare Workers

Build edge APIs with Cloudflare Workers.

## When to Use

- Global low-latency API endpoints
- Auth, routing, and caching at the edge
- Serverless functions near users

## Scaffold

```bash
npx wrangler init my-worker
cd my-worker
npx wrangler dev
```

## Handler

```ts
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);
    if (url.pathname === "/health") {
      return new Response(JSON.stringify({ ok: true }), {
        headers: { "Content-Type": "application/json" },
      });
    }
    const key = url.pathname.slice(1);
    return new Response(`Hello from edge: ${key}`);
  },
};
```

## Deploy

```bash
npx wrangler deploy --dry-run
npx wrangler deploy
npx wrangler deployments list
```

## Secrets and Bindings

```bash
npx wrangler secret put API_KEY
npx wrangler tail
npx wrangler kv key list --binding=MY_KV
```

## wrangler.toml

```toml
name = "my-worker"
main = "src/index.ts"
compatibility_date = "2025-01-01"

[[kv_namespaces]]
binding = "MY_KV"
id = "xxxxxxxx"
```

## Testing

```bash
npx wrangler dev &
curl -s http://localhost:8787/health | jq
npx wrangler tail --format json
```

## Best Practices

- Use --dry-run before real deploys
- Keep secrets in wrangler secret put, never in code
- Set compatibility dates explicitly
- Test with Miniflare in CI
- Cache aggressively with the Cache API
- Use Durable Objects for stateful services
- Watch usage with wrangler deployments and analytics

## Capabilities

### wrangler-dev
Scaffold Workers projects, run locally, and deploy to the edge

**Commands:**
- `npx wrangler init my-worker`
- `npx wrangler dev`
- `npx wrangler deploy`
- `npx wrangler whoami`

**Examples:**
- npx wrangler init my-worker --yes && npx wrangler dev
- npx wrangler deploy --dry-run
- npx wrangler whoami

### runtime-tools
Manage secrets, inspect live traffic, and check KV/Durable Object bindings

**Commands:**
- `npx wrangler secret put API_KEY`
- `npx wrangler tail`
- `npx wrangler kv key list --binding=MY_KV`
- `npx wrangler deployments list`

**Examples:**
- npx wrangler secret put API_KEY
- npx wrangler tail --format json
- npx wrangler kv key list --binding=MY_KV | jq '.keys[0].name'
