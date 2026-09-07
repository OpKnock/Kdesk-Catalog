---
trigger: glob
description: "Builds full-stack React apps with Remix: loaders, actions, server rendering, and deployment to Node/Cloudflare. Use when working with scaffold, build deploy, frontend or when the user mentions scaffold, build deploy, frontend."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

Builds full-stack React apps with Remix: loaders, actions, server rendering, and deployment to Node/Cloudflare.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx create-remix@latest my-app --template remix-run/remix/te`, `npx remix build`
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

# Remix

Build full-stack React apps where data loading and mutations live next to the UI.

## When to Use

- Apps with heavy server data dependencies
- Progressive enhancement with native forms
- SSR-first SEO-sensitive pages

## Scaffold

```bash
npx create-remix@latest my-app --template remix-run/remix/templates/express
npm run dev
```

## Loaders and actions

```tsx
// app/routes/orders._index.tsx
import { json } from '@remix-run/node';
import { useLoaderData, Form } from '@remix-run/react';

export async function loader() {
  const orders = await db.order.findMany();
  return json({ orders });
}

export async function action({ request }: ActionFunctionArgs) {
  const fd = await request.formData();
  await db.order.create({ data: { sku: String(fd.get('sku')) } });
  return json({ ok: true });
}
```

## Route tree

```bash
npx remix routes
```

## Build and serve

```bash
npx remix build
npx remix-serve build/server/index.js
```

## Best practices

- Load minimal data per route; let nesting compose the page.
- Prefer Form actions over fetch for mutations to get progressive enhancement.
- Set `shouldRevalidate` carefully to avoid refetch storms.
- Type-check before build: `npm run typecheck && npx remix build`.

## Testing

```bash
npm run typecheck
npx remix build
```

Run both in CI; a failed typecheck with a passing build indicates stale types.

## Capabilities

### scaffold
Create and configure Remix applications.

**Parameters:**
- `template` (string): Deployment template: express, cloudflare, netlify, vercel
- `json` (string): Print route tree as JSON
- `show` (string): Preview revealed files without writing

**Commands:**
- `npx create-remix@latest my-app --template remix-run/remix/templates/express`
- `npm run dev`
- `npx remix reveal`
- `npx remix routes`
- `npx remix vite:dev`

**Examples:**
- npx create-remix@latest store --template remix-run/remix/templates/cloudflare-pages
- npx remix routes --json
- npx remix reveal --show

### build-deploy
Build and run Remix apps for production.

**Parameters:**
- `sourcemap` (string): Emit sourcemaps for the build
- `port` (number): Production server port
- `build` (string): Build mode: development or production

**Commands:**
- `npx remix build`
- `npx remix-serve build/server/index.js`
- `npm run start`
- `npx remix build && npx remix-serve build/server/index.js`
- `npm run typecheck && npx remix build`

**Examples:**
- npx remix build --sourcemap
- npx remix-serve build/server/index.js --port 3001
- npm run typecheck && npx remix build

## References
- [Remix Docs](https://remix.run/docs)
- [Remix CLI](https://remix.run/docs/en/main/other-api/cli)
- [Remix Deployment](https://remix.run/docs/en/main/guides/deployment)
