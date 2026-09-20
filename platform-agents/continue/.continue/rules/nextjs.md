---
name: "nextjs"
description: "Builds full-stack React apps with Next.js App Router: server components, route handlers, middleware, and Vercel/Docker deploys."
globs: ["**/*.json", "**/*.r", "**/*.sh", "**/*.{ts,tsx}"]
alwaysApply: false
---

# nextjs

Builds full-stack React apps with Next.js App Router: server components, route handlers, middleware, and Vercel/Docker deploys.

## Instructions

# Next.js

Build full-stack React applications with Next.js App Router and real CLI.

## When to Use

- React apps needing SSR/SSG and API routes
- Marketing + app hybrids with incremental static regeneration
- Teams standardizing on one full-stack React framework

## Scaffold

```bash
npx create-next-app@latest my-app --typescript --tailwind --eslint --app --src-dir
npm run dev
```

## Server Components and data fetching

```tsx
// app/products/page.tsx
export default async function Products() {
  const res = await fetch('https://api.example.com/products', { next: { revalidate: 300 } });
  const products = await res.json();
  return <ul>{products.map(p => <li key={p.id}>{p.name}</li>)}</ul>;
}
```

Use `revalidate` for ISR, `cache: 'no-store'` for dynamic data.

## Route handlers

```typescript
// app/api/orders/route.ts
import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  const body = await request.json();
  return NextResponse.json({ ok: true, id: body.id }, { status: 201 });
}
```

## Middleware

```typescript
// middleware.ts
export function middleware(request: NextRequest) {
  const token = request.cookies.get('token');
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
  return NextResponse.next();
}
```

## Build and deploy

```bash
npm run build
npx next build --debug

# Vercel
vercel --prod

# Docker
docker build -t myapp .
docker run -p 3000:3000 myapp
```

## Best practices

- Move client interactivity to `use client` boundaries; keep the rest server components.
- Set `next/font` to self-host fonts and avoid layout shift.
- Gate merges on `npm run lint` and `npm run build`.
- Use `next info` when diagnosing version/env issues.

## Testing

```bash
npm run build
npm run lint
```

Run both in CI before deploying to any environment.

## Capabilities

### scaffold-dev
Create, run, and lint Next.js projects.

**Commands:**
- `npx create-next-app@latest my-app --typescript --tailwind --eslint --app --src-dir`
- `npm run dev`
- `npm run build`
- `npm run lint`
- `npm run start`

**Examples:**
- npx create-next-app@latest store --typescript --app --no-tailwind
- npm run dev -- --port 3100
- npm run build && npm run start

### diagnose
Inspect Next.js setup and build output.

**Commands:**
- `npx next info`
- `npx next lint --dir src`
- `npx next build --debug`
- `npx next dev --turbo`
- `npx next telemetry disable`

**Examples:**
- npx next info | grep -i versions
- npx next lint --file src/app/page.tsx --fix
- npx next dev --turbo --port 3000