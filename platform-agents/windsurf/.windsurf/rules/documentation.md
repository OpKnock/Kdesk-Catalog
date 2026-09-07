---
trigger: glob
description: "Authors and publishes project documentation sites with MkDocs: scaffolds, previews with hot reload, builds strictly, and deploys to GitHub Pages. Use when working with mkdocs publishing, api or when the user mentions mkdocs publishing, api."
globs: ["**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

Authors and publishes project documentation sites with MkDocs: scaffolds, previews with hot reload, builds strictly, and deploys to GitHub Pages.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `mkdocs new my-docs`
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

# Documentation

## What this skill does

This skill covers authoring and publishing documentation sites with MkDocs: project scaffolding, live preview, strict builds, and GitHub Pages deployment. Markdown files are the source of truth.

## When to use

- Starting a docs site for a project, API, or team
- Restructuring an existing docs tree
- Publishing docs to GitHub Pages or a static host

## Real commands

```bash
# Scaffold a new project
 mkdocs new my-docs
 cd my-docs

# Preview with hot reload
 mkdocs serve --dev-addr 127.0.0.1:8000

# Build the static site (strict = warnings become errors)
 mkdocs build --clean
 mkdocs build --strict

# Deploy to GitHub Pages
 mkdocs gh-deploy --force
```

## mkdocs.yml example

```yaml
site_name: My Project
theme:
  name: material
  features:
    - navigation.tabs
    - search.suggest
nav:
  - Home: index.md
  - Guides:
      - Getting started: guides/getting-started.md
      - Configuration: guides/configuration.md
plugins:
  - search
markdown_extensions:
  - admonition
  - pymdownx.superfences
```

## Writing guidelines

- One idea per page; link between pages instead of duplicating.
- Keep a short title and an intro sentence before any heading.
- Use admonitions (note, warning) sparingly for emphasis.
- Include a code example on every how-to page.

## Testing

```bash
# Verify every link resolves and no warnings are emitted
 mkdocs build --strict && echo 'docs healthy'
```

## Best practices

- Use `mkdocs build --strict` in CI so broken links fail the pipeline.
- Keep nav ordering in mkdocs.yml aligned with the docs tree.
- Preview locally before every `gh-deploy`.
- Store docs beside the code and version them together.

## Capabilities

### mkdocs-publishing
Scaffold, serve, build, and deploy MkDocs documentation projects.

**Parameters:**
- `project-dir` (string): Directory where the docs project lives
- `dev-addr` (string): Host:port for the local preview server
- `strict-mode` (boolean): Treat warnings as errors during build

**Commands:**
- `mkdocs new my-docs`
- `mkdocs serve --dev-addr 127.0.0.1:8000`
- `mkdocs build --clean`
- `mkdocs gh-deploy`
- `mkdocs build --strict`
- `mkdocs --version`

**Examples:**
- mkdocs new my-docs && cd my-docs && mkdocs serve
- mkdocs build --strict
- mkdocs gh-deploy --force

## References
- [MkDocs Documentation](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
