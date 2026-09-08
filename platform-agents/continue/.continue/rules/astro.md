---
name: "Astro"
description: "Builds content-focused websites and islands-architecture apps with Astro: content collections, integrations, and static builds. Use when working with scaffold, build preview, frontend or when the user mentions scaffold, build preview, frontend."
globs: ["**/*.r", "**/*.sh", "**/*.{ts,tsx}"]
alwaysApply: false
---

Builds content-focused websites and islands-architecture apps with Astro: content collections, integrations, and static builds.

## Agentic Workflow: Read -> Reason -> Act (astro)

You are **Astro** (frontend/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — frontend context for `astro`
- Domain: Builds content-focused websites and islands-architecture apps with Astro: content collections, integrations, and static builds.
- **scaffold**: Create Astro projects and add framework integrations. — `npm create astro@latest -- --template minimal --no-git --install`
- **build-preview**: Develop, type-check, build, and preview Astro sites. — `npm run dev`
- Check `knowledge` and `prerequisites: npm, npx`

### 2. Reason — think for `astro`
- For `scaffold`: Create Astro projects and add framework integrations. — decide which checks to run
- For `build-preview`: Develop, type-check, build, and preview Astro sites. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `astro` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `astro:2d67e292`

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

**Parameters:**
- `template` (string): minimal, blog, docs, or portfolio starter
- `install` (string): --install to auto-install dependencies
- `no-git` (string): Skip git initialization

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

**Parameters:**
- `port` (number): Dev/preview server port
- `minimumSeverityLevel` (string): astro check severity gate: hint, warning, error
- `output` (string): static (default) or server for SSR

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

## References
- [Astro Docs](https://docs.astro.build/en/getting-started/)
- [Astro Content Collections](https://docs.astro.build/en/guides/content-collections/)
- [Astro CLI](https://docs.astro.build/en/reference/cli-reference/)