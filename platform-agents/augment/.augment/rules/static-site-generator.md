---
type: agent_requested
description: "Builds and serves static sites with Hugo and Eleventy, managing content, themes, and production builds. Use when working with hugo build, eleventy build, content publishing or when the user mentions hugo build, eleventy build, content publishing."
---

Builds and serves static sites with Hugo and Eleventy, managing content, themes, and production builds.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `hugo new site mysite`, `npx @11ty/eleventy --input=src --output=dist`
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

**Parameters:**
- `draft` (boolean): Include draft content (-D)
- `minify` (boolean): Minify output HTML/CSS/JS
- `baseURL` (string): Site base URL for the build

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

**Parameters:**
- `input` (string): Source content directory
- `output` (string): Output directory
- `pathprefix` (string): Sub-path prefix for the site

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

**Parameters:**
- `gc` (boolean): Clean up generated cache
- `outputDir` (string): Destination directory for the generated site.

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

## References
- [Hugo Documentation](https://gohugo.io/documentation/)
- [Eleventy Documentation](https://www.11ty.dev/docs/)