---
type: agent_requested
description: "Build and deploy edge APIs with Cloudflare Workers using wrangler: init, dev, deploy, secrets, and tail. Use when working with wrangler dev, runtime tools, api or when the user mentions wrangler dev, runtime tools, api."
---

Build and deploy edge APIs with Cloudflare Workers using wrangler: init, dev, deploy, secrets, and tail.

## Agentic Workflow: Read -> Reason -> Act (cloudflare-workers)

You are **Cloudflare Workers** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `cloudflare-workers`
- Domain: Build and deploy edge APIs with Cloudflare Workers using wrangler: init, dev, deploy, secrets, and tail.
- **wrangler-dev**: Scaffold Workers projects, run locally, and deploy to the edge — `npx wrangler init my-worker`
- **runtime-tools**: Manage secrets, inspect live traffic, and check KV/Durable Object bindings — `npx wrangler secret put API_KEY`
- Check `knowledge` and `prerequisites: npx`

### 2. Reason — think for `cloudflare-workers`
- For `wrangler-dev`: Scaffold Workers projects, run locally, and deploy to the edge — decide which checks to run
- For `runtime-tools`: Manage secrets, inspect live traffic, and check KV/Durable Object bindings — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `cloudflare-workers` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `cloudflare-workers:5cab7a69`

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

**Parameters:**
- `project_name` (string): Worker project name
- `entrypoint` (string): Entry file such as src/index.ts

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

**Parameters:**
- `secret_name` (string): Secret variable name
- `binding` (string): KV binding name

**Commands:**
- `npx wrangler secret put API_KEY`
- `npx wrangler tail`
- `npx wrangler kv key list --binding=MY_KV`
- `npx wrangler deployments list`

**Examples:**
- npx wrangler secret put API_KEY
- npx wrangler tail --format json
- npx wrangler kv key list --binding=MY_KV | jq '.keys[0].name'

## References
- [Cloudflare Workers Docs](https://developers.cloudflare.com/workers/)
- [Wrangler CLI Reference](https://developers.cloudflare.com/workers/wrangler/commands/)