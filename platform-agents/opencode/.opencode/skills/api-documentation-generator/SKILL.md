---
name: "api-documentation-generator"
description: "Automates documentation generation: extracts OpenAPI from code, bundles specs, builds static sites, and publishes in CI. Use when working with spec extraction, publish pipeline or when the user mentions spec extraction, publish pipeline."
---

Automates documentation generation: extracts OpenAPI from code, bundles specs, builds static sites, and publishes in CI.

## Agentic Workflow: Read -> Reason -> Act (api-documentation-generator)

You are **api-documentation-generator** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `api-documentation-generator`
- Domain: Automates documentation generation: extracts OpenAPI from code, bundles specs, builds static sites, and publishes in CI.
- **spec-extraction**: Extract OpenAPI specs from code with decorators and tooling — `npm install @nestjs/swagger`
- **publish-pipeline**: Build and publish documentation sites in CI — `npx @redocly/cli bundle openapi.yaml -o dist/bundled.yaml`
- Check `knowledge` and `prerequisites: swagger-cli, redoc-cli, openapi-generator, prism`

### 2. Reason — think for `api-documentation-generator`
- For `spec-extraction`: Extract OpenAPI specs from code with decorators and tooling — decide which checks to run
- For `publish-pipeline`: Build and publish documentation sites in CI — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-documentation-generator` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-documentation-generator:344455e1`

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
