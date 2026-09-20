---
name: "developer-portal"
description: "Builds and maintains API developer portals: lint and bundle OpenAPI specs with Redocly, validate with swagger-cli, and publish static documentation with Docusaurus. Use when working with spec publishing, api or when the user mentions spec publishing, api."
license: "MIT"
compatibility: "Requires npx."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(npx:*)"
---

Builds and maintains API developer portals: lint and bundle OpenAPI specs with Redocly, validate with swagger-cli, and publish static documentation with Docusaurus.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx @redocly/cli lint openapi.yaml`
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

# Developer Portal

## What this skill does

A developer portal is the single place where API consumers discover endpoints, read reference docs, and get API keys. This skill covers spec validation, portal rendering, and publishing workflows using Redocly, swagger-cli, and Docusaurus.

## When to use

- Setting up a new API documentation portal from an OpenAPI spec

- Running spec quality checks before merging changes into the portal

- Releasing a new version of API reference docs

## Real commands

```bash
# Validate and lint the spec
npx swagger-cli validate openapi.yaml
npx @redocly/cli lint openapi.yaml

# Bundle multi-file specs into one
npx @redocly/cli bundle openapi.yaml -o dist/openapi.bundle.yaml

# Generate a standalone HTML reference page
npx @redocly/cli build-docs openapi.yaml -o public/index.html

# Split a big spec into multi-file structure
npx @redocly/cli split openapi.yaml --out-dir ./split
```

## Docusaurus publishing

```bash
# Copy the rendered page into the Docusaurus static folder
npx @redocly/cli build-docs openapi.yaml -o docs/static/api/index.html
npx docusaurus build
npx docusaurus deploy
```

## Best practices

- Run `swagger-cli validate` in CI on every spec commit.

- Keep specs in a separate repo so the portal can version them independently.

- Use Redocly config files (redocly.yaml) to pin decorators and rules per project.

- Generate the reference page from a bundled spec to avoid relative $ref breakage.

- Add an API key onboarding page next to the reference docs.

## Testing

```bash
# Serve the built portal locally and verify it loads
npx @redocly/cli preview-docs openapi.yaml
```

## Capabilities

### spec-publishing
Validate, lint, bundle, and render OpenAPI specifications into developer portal pages.

**Parameters:**
- `spec-file` (string): Path to the OpenAPI 3.x spec file
- `output-dir` (string): Directory for generated portal assets
- `theme` (string): Redocly theme name or custom theme file for docs styling

**Commands:**
- `npx @redocly/cli lint openapi.yaml`
- `npx @redocly/cli bundle openapi.yaml -o dist/openapi.bundle.yaml`
- `npx @redocly/cli build-docs openapi.yaml -o public/index.html`
- `npx swagger-cli validate openapi.yaml`
- `npx @redocly/cli split openapi.yaml --out-dir ./split`

**Examples:**
- npx @redocly/cli lint openapi.yaml && npx @redocly/cli build-docs openapi.yaml -o public/index.html
- npx swagger-cli validate openapi.yaml
- npx @redocly/cli bundle openapi.yaml -o dist/openapi.bundle.yaml

## References
- [Redocly CLI Reference](https://redocly.com/docs/cli/commands/lint/)
