---
name: "cloudflare-workers"
description: "Build and deploy edge APIs with Cloudflare Workers using wrangler: init, dev, deploy, secrets, and tail. Use when working with wrangler dev, runtime tools, api or when the user mentions wrangler dev, runtime tools, api."
---

Build and deploy edge APIs with Cloudflare Workers using wrangler: init, dev, deploy, secrets, and tail.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx wrangler init my-worker`, `npx wrangler secret put API_KEY`
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
