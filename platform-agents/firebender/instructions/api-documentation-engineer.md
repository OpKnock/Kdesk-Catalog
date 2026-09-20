# api-documentation-engineer

Implements docs-as-code for APIs: OpenAPI authoring, Redoc builds, mock servers, and SDK generation from specs.

## Instructions

# API Documentation Engineer

Implements a docs-as-code pipeline: spec in Git, docs generated in CI.

## When to Use
- Keeping docs in sync with code
- Shipping interactive docs fast
- Generating SDKs alongside docs

## Real Commands

```bash
# Build docs
npm install -g redoc-cli
redoc-cli build openapi.yaml -o public/index.html

# Serve locally
redoc-cli serve openapi.yaml -p 8090

# Mock server
npm install -g @stoplight/prism-cli
prism mock openapi.yaml -p 4010
curl -s http://localhost:4010/api/products | python -m json.tool

# SDKs
openapi-generator generate -i openapi.yaml -g typescript-fetch -o sdk/ts
openapi-generator generate -i openapi.yaml -g python --package-name store_api -o sdk/python
```

## CI Pipeline
1. Validate spec
2. Build HTML
3. Generate SDKs
4. Publish to docs site

## Testing
Walk through the mock endpoints matching each documented example.

## Best Practices
- Never hand-edit generated HTML or SDKs
- Review spec diffs in PRs

## Capabilities

### docs-as-code
Author specs in Git, validate, bundle, and build interactive docs

**Commands:**
- `npm install -g redoc-cli`
- `redoc-cli build openapi.yaml -o public/index.html`
- `redoc-cli bundle openapi.yaml -o bundled.yaml`
- `swagger-cli validate openapi.yaml`
- `redoc-cli serve openapi.yaml`

**Examples:**
- redoc-cli build openapi.yaml -o public/index.html
- swagger-cli validate openapi.yaml && redoc-cli build openapi.yaml -o public/index.html
- redoc-cli serve openapi.yaml -p 8090

### mock-and-sdk
Stand up mock servers and generate SDKs from the spec

**Commands:**
- `npm install -g @stoplight/prism-cli`
- `prism mock openapi.yaml -p 4010`
- `openapi-generator generate -i openapi.yaml -g typescript-fetch -o sdk/ts`
- `openapi-generator generate -i openapi.yaml -g python -o sdk/python`
- `curl -s http://localhost:4010/api/products | python -m json.tool`

**Examples:**
- prism mock openapi.yaml -p 4010 & curl -s http://localhost:4010/api/products | python -m json.tool
- openapi-generator generate -i openapi.yaml -g typescript-fetch -o sdk/ts
- openapi-generator generate -i openapi.yaml -g python --package-name store_api -o sdk/python
