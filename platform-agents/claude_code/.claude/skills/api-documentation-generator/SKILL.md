---
name: "api-documentation-generator"
description: "Automates documentation generation: extracts OpenAPI from code, bundles specs, builds static sites, and publishes in CI. Use when working with spec extraction, publish pipeline or when the user mentions spec extraction, publish pipeline."
license: "MIT"
compatibility: "Requires swagger-cli, redoc-cli, openapi-generator, prism, stoplight-studio, postman."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "backend"}
allowed-tools: "Glob Grep Read Bash(node:*) Bash(npm:*) Bash(npx:*) Bash(pip:*)"
---

Automates documentation generation: extracts OpenAPI from code, bundles specs, builds static sites, and publishes in CI.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm install @nestjs/swagger`, `npx @redocly/cli bundle openapi.yaml -o dist/bundled.yaml`
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

# API Documentation Generator

Automates docs from code to static site with zero hand-written reference content.

## When to Use
- Docs drift from code constantly
- Reference docs must be generated
- Publishing docs in CI

## Real Commands

```bash
# Extract from FastAPI
python -c "from fastapi.openapi.utils import get_openapi;print('fastapi openapi ready')"

# Extract from Express
npm install swagger-autogen

# Bundle and lint
npx @redocly/cli bundle openapi.yaml -o dist/bundled.yaml
npx @redocly/cli lint dist/bundled.yaml

# Build site
npx @redocly/cli build-docs dist/bundled.yaml -o dist/index.html
npm install -g docusaurus && npx docusaurus build
```

## CI Flow
1. Extract spec from code
2. Lint and bundle
3. Build reference pages
4. Publish to hosting

## Testing
Compare generated docs against the running API automatically.

## Best Practices
- Generation in CI on every merge
- Keep hand-written guides separate from generated reference

## Capabilities

### spec-extraction
Extract OpenAPI specs from code with decorators and tooling

**Parameters:**
- `framework` (string): FastAPI, NestJS, Express
- `output` (string): Spec output path

**Commands:**
- `npm install @nestjs/swagger`
- `npm install swagger-autogen`
- `node -e "const a=require('swagger-autogen')();console.log(typeof a)"`
- `pip install fastapi && python -c "from fastapi.openapi.utils import get_openapi;print('fastapi openapi ready')"`
- `node -e "console.log('swagger-autogen -o ./swagger.json')"`

**Examples:**
- npm install swagger-autogen && node -e "const a=require('swagger-autogen')();console.log(typeof a)"
- pip install fastapi && python -c "from fastapi.openapi.utils import get_openapi;print('fastapi openapi ready')"
- npm install @nestjs/swagger

### publish-pipeline
Build and publish documentation sites in CI

**Parameters:**
- `spec` (string): Source OpenAPI spec
- `outputDir` (string): Static site output

**Commands:**
- `npx @redocly/cli bundle openapi.yaml -o dist/bundled.yaml`
- `npx @redocly/cli build-docs dist/bundled.yaml -o dist/index.html`
- `npx @redocly/cli lint dist/bundled.yaml`
- `npm install -g docusaurus`
- `npx docusaurus build`

**Examples:**
- npx @redocly/cli bundle openapi.yaml -o dist/bundled.yaml && npx @redocly/cli build-docs dist/bundled.yaml -o dist/index.html
- npx @redocly/cli lint dist/bundled.yaml
- npm install -g docusaurus && npx docusaurus build

## References
- [swagger-autogen](https://github.com/davibaltar/swagger-autogen)
- [FastAPI OpenAPI](https://fastapi.tiangolo.com/advanced/openapi-callbacks/)
- [Docusaurus](https://docusaurus.io/docs)
