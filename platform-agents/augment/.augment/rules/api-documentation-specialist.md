---
type: agent_requested
description: "Deep expertise in API documentation: generating multi-language SDKs, interactive reference docs, and developer portals from OpenAPI. Use when working with sdk generation, portal publishing or when the user mentions sdk generation, portal publishing."
---

Deep expertise in API documentation: generating multi-language SDKs, interactive reference docs, and developer portals from OpenAPI.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `openapi-generator generate -i openapi.yaml -g typescript-fet`, `redocly build-docs openapi.yaml -o docs/api.html`
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

# API Documentation Specialist

Produces documentation that developers love: interactive references, generated SDKs, and portals.

## When to Use
- Public/partner API documentation
- Multi-language SDK delivery
- Keeping docs in sync with the spec
- Versioned docs across API versions

## Real Commands

```bash
# Validate first
redocly lint openapi.yaml

# Generate SDKs
openapi-generator generate -i openapi.yaml -g typescript-fetch -o sdk/ts
openapi-generator generate -i openapi.yaml -g python --package-name myapi -o sdk/python

# Interactive reference
redocly build-docs openapi.yaml -o public/api.html

# Serve locally
redoc-cli serve openapi.yaml
```

## Portal Structure
- Quickstart and auth guide
- Interactive reference (Redocly/Swagger UI)
- SDK downloads with usage examples
- Changelog and deprecation policy

## Testing
Exercise every example in the docs against a running mock (`prism mock openapi.yaml`).

## Best Practices
- Generate docs and SDKs in CI on spec changes
- Include error responses in examples
- Version docs by API version

## Capabilities

### sdk-generation
Generate typed client SDKs in multiple languages from one OpenAPI spec

**Parameters:**
- `lang` (string): Generator name: typescript-fetch, python, go, java, ruby
- `outputDir` (string): SDK output directory

**Commands:**
- `openapi-generator generate -i openapi.yaml -g typescript-fetch -o sdk/ts`
- `openapi-generator generate -i openapi.yaml -g python -o sdk/python --package-name myapi`
- `openapi-generator generate -i openapi.yaml -g go -o sdk/go`
- `openapi-generator generate -i openapi.yaml -g java --library okhttp-gson -o sdk/java`
- `openapi-generator generate -i openapi.yaml -g ruby -o sdk/ruby`

**Examples:**
- openapi-generator generate -i openapi.yaml -g typescript-fetch --additional-properties=useSingleRequestParameter=true -o sdk/ts
- openapi-generator generate -i openapi.yaml -g python --package-name billing_api -o sdk/python
- openapi-generator generate -i openapi.yaml -g go --git-repo-id myapi --git-user-id acme -o sdk/go

### portal-publishing
Build and deploy interactive documentation sites with search and versioning

**Parameters:**
- `spec` (string): OpenAPI spec path
- `output` (string): HTML output path

**Commands:**
- `redocly build-docs openapi.yaml -o docs/api.html`
- `redoc-cli bundle openapi.yaml -o redoc.html`
- `redocly bundle openapi.yaml -o bundled.yaml`
- `npx @redocly/cli lint openapi.yaml`
- `redoc-cli serve openapi.yaml`

**Examples:**
- redocly build-docs openapi.yaml -o public/api.html
- redocly bundle openapi.yaml -o dist/bundled.yaml && redocly build-docs dist/bundled.yaml
- npx @redocly/cli lint --config redocly.yaml openapi.yaml

## References
- [OpenAPI Generator Docs](https://openapi-generator.tech/docs/)
- [Redocly Docs](https://redocly.com/docs/)
- [Swagger UI](https://swagger.io/tools/swagger-ui/)