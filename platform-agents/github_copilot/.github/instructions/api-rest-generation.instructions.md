---
applyTo: "**/*.go **/*.html **/*.java **/*.py **/*.r **/*.sh **/*.{ts,tsx} **/*.{yaml,yml}"
---

Generates REST clients and documentation from OpenAPI with openapi-generator-cli and Redocly: multi-language client generation, config files, and docs deployment.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx @openapitools/openapi-generator-cli generate -i openapi.`, `npx @redocly/cli build-docs openapi.yaml -o dist/api.html`
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

# API REST v5 - Clients & Docs

Code and doc generation from OpenAPI.

## What This Skill Does
- Generates clients for TS, Python, Go, Java
- Builds static docs from the spec
- Keeps generated artifacts in sync

## When to Use
- Releasing official SDKs
- Sharing docs with consumers
- Multi-language client support

## Real Commands

```bash
npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g typescript-fetch -o ./client-ts
npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g python -o ./client-py
npx @redocly/cli build-docs openapi.yaml -o dist/api.html
```

## Generation Config

```yaml
inputSpec: openapi.yaml
generators:
  typescript-fetch:
    output: client-ts
    additionalProperties:
      useSingleRequestParameter: true
```

## Testing
- Compile each generated client
- Run a smoke call against the live API
- Diff generated output on spec changes

## Best Practices
- Commit generated clients in SDK repos
- Regenerate on tagged releases only
- Validate specs before generation

## Capabilities

### client-generation
Generate typed API clients in multiple languages

**Parameters:**
- `input-spec` (string): OpenAPI file path
- `generator` (string): Target language generator
- `output` (string): Output directory

**Commands:**
- `npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g typescript-fetch -o ./client-ts`
- `npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g python -o ./client-py`
- `npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g go -o ./client-go`
- `npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g java -o ./client-java`
- `npx @openapitools/openapi-generator-cli config-help -g typescript-fetch`

**Examples:**
- -g typescript-fetch produces a fetch-based TS client
- -g python generates a requests-based client
- config-help documents generator options

### docs-deployment
Build and preview reference documentation

**Commands:**
- `npx @redocly/cli build-docs openapi.yaml -o dist/api.html`
- `npx @redocly/cli preview-docs openapi.yaml`
- `npx @redocly/cli bundle openapi.yaml -o dist/openapi.bundle.yaml`
- `npx @redocly/cli lint openapi.yaml`

**Examples:**
- -cli --help
- -api --help

## References
- [OpenAPI Generator CLI](https://openapi-generator.tech/docs/usage/)
- [Redocly CLI](https://redocly.com/docs/cli/)
