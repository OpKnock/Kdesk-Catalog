---
name: "astro"
description: "Builds content-focused websites and islands-architecture apps with Astro: content collections, integrations, and static builds."
type: knowledge
triggers: ["astro", "scaffold", "build-preview"]
---

# Astro

Builds content-focused websites and islands-architecture apps with Astro: content collections, integrations, and static builds.

## Instructions

# Astro

Build fast content sites and island-architecture apps with Astro.

## When to Use

- Blogs, docs, marketing sites, portfolios
- Hybrid sites that mix static content with interactive islands
- Sites needing excellent Core Web Vitals out of the box

## Create a project

```bash
npm create astro@latest -- --template minimal --no-git
npx astro add react tailwind sitemap
```

## Content collections

```typescript
// src/content.config.ts
import { defineCollection, z } from 'astro:content';

export const collections = {
  posts: defineCollection({
    type: 'content',
    schema: z.object({
      title: z.string(),
      pubDate: z.coerce.date(),
      tags: z.array(z.string()).default([]),
      draft: z.boolean().default(false)
    })
  })
};
```

```bash
npx astro sync
```

Sync regenerates content types - run it after editing schemas.

## Islands

Interactive components render only when they need hydration:

```tsx
import Counter from '../components/Counter.tsx';
<Counter client:load />
```

Use `client:idle`, `client:visible`, or `client:only="react"` to control when JS ships.

## Build and check

```bash
npx astro check --minimumSeverityLevel error
npm run build
npx astro preview
```

## Best practices

- Prefer Markdown/MDX for content; components for layout.
- Add `@astrojs/sitemap` and `astro:env` for production config.
- Set `output: 'static'` unless you need SSR.
- Always run `astro check` in CI before deploy.

## Capabilities

### scaffold
Create Astro projects and add framework integrations.

**Commands:**
- `npm create astro@latest -- --template minimal --no-git --install`
- `npx astro add react`
- `npx astro add tailwind`
- `npx astro add sitemap`
- `npx astro add @astrojs/mdx`

**Examples:**
- npm create astro@latest -- --template blog --install --no-git
- npx astro add react --yes
- npx astro add vercel

### build-preview
Develop, type-check, build, and preview Astro sites.

**Commands:**
- `npm run dev`
- `npx astro check`
- `npm run build`
- `npx astro preview`
- `npx astro sync`

**Examples:**
- npm run dev -- --port 4321
- npx astro check --minimumSeverityLevel error
- npm run build && npx astro preview --port 8080
