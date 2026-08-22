---
name: "static-site-generator"
description: "Builds and serves static sites with Hugo and Eleventy, managing content, themes, and production builds."
globs: ["**/*.go", "**/*.r", "**/*.sh"]
alwaysApply: false
---

# static-site-generator

Builds and serves static sites with Hugo and Eleventy, managing content, themes, and production builds.

## Instructions

# Static Site Generation

Build fast static sites with Hugo and Eleventy.

## What This Skill Does

- Scaffolds sites and content with Hugo/Eleventy CLIs
- Serves live-preview dev servers with drafts
- Produces minified production builds
- Manages taxonomies, drafts, and git-based deploy info

## When to Use

- Creating documentation or marketing sites
- Migrating a slow dynamic site to static
- Building a blog with markdown content

## Real Commands

```bash
# Hugo
hugo new site mysite
hugo new posts/first-post.md
hugo server -D
hugo -D --minify
hugo --gc --minify --enableGitInfo
hugo list drafts

# Eleventy
npx @11ty/eleventy --input=src --output=dist
npx @11ty/eleventy --serve
npx @11ty/eleventy --config=.eleventy.cjs --pathprefix=/blog
```

## Hugo Config (hugo.toml)

```toml
baseURL = "https://example.com/"
title = "Docs"
enableGitInfo = true
[minify]
  minifyOutput = true
[params]
  description = "Product documentation"
```

## Best Practices

- Keep content in markdown with front matter for metadata
- Build with --minify and --gc for production
- Set --enableGitInfo so pages show last-modified dates
- Use a single content directory convention per team
- Deploy the static output via any CDN or object storage

## Capabilities

### hugo-build
Scaffold, develop, and build Hugo sites.

**Commands:**
- `hugo new site mysite`
- `hugo new posts/first-post.md`
- `hugo server -D`
- `hugo -D`
- `hugo list all`

**Examples:**
- hugo new site mysite && cd mysite && hugo server -D
- hugo new posts/hello-world.md
- hugo -D --minify

### eleventy-build
Scaffold, serve, and build Eleventy sites.

**Commands:**
- `npx @11ty/eleventy --input=src --output=dist`
- `npx @11ty/eleventy --serve`
- `npx @11ty/eleventy --watch`
- `npx @11ty/eleventy --quiet`
- `npx @11ty/eleventy --config=.eleventy.cjs --pathprefix=/docs`

**Examples:**
- npx @11ty/eleventy --input=src --output=dist
- npx @11ty/eleventy --serve
- npx @11ty/eleventy --pathprefix=/blog

### content-publishing
Manage content, taxonomies, and deployment output.

**Commands:**
- `hugo new docs/guide/_index.md`
- `hugo --gc --minify --enableGitInfo`
- `hugo list drafts`
- `hugo config`
- `hugo env`

**Examples:**
- hugo --gc --minify --enableGitInfo
- hugo list drafts
- hugo config