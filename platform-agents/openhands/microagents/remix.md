---
name: "remix"
description: "Builds full-stack React apps with Remix: loaders, actions, server rendering, and deployment to Node/Cloudflare."
type: knowledge
triggers: ["remix", "scaffold", "build-deploy"]
---

# Remix

Builds full-stack React apps with Remix: loaders, actions, server rendering, and deployment to Node/Cloudflare.

## Instructions

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
