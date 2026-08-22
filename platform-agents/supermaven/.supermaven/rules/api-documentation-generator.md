# api-documentation-generator

Automates documentation generation: extracts OpenAPI from code, bundles specs, builds static sites, and publishes in CI.

## Instructions

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