---
applyTo: "**/*.html **/*.json **/*.r **/*.sh **/*.{yaml,yml}"
---

# Api Doc Openapi Authoring

Implements API documentation basics: OpenAPI authoring, Swagger UI/Redoc serving, and first docs build. Use when authoring or serving OpenAPI specs. Don't use for docs-site architecture (see api-doc-site-architecture) or generated SDK docs (see api-documentation-generator).

## Instructions

# API Doc (Implementation)

Gets documentation on its feet: a validated spec and a served UI.

## When to Use
- No docs exist yet
- Quick reference docs for a service
- Single-spec documentation

## Real Commands

```bash
# Validate
npm install -g swagger-cli
swagger-cli validate openapi.yaml

# Bundle for distribution
swagger-cli bundle openapi.yaml -o bundled.yaml

# Serve Redoc
npm install -g redoc-cli
redoc-cli serve openapi.yaml -p 8090

# Build static HTML
redoc-cli build openapi.yaml -o index.html

# Swagger UI
npm install swagger-ui-dist
```

## Minimal Spec

```yaml
openapi: 3.0.0
info:
  title: My API
  version: 1.0.0
paths: {}
```

## Testing
Validate after every spec edit; keep bundled.yaml committed.

## Best Practices
- Validate in pre-commit
- Serve the same bundled file in all environments

## Capabilities

### openapi-authoring
Author and validate OpenAPI specs by hand or from code

**Commands:**
- `npm install -g swagger-cli`
- `swagger-cli validate openapi.yaml`
- `swagger-cli bundle openapi.yaml -o bundled.yaml`
- `swagger-cli dereference openapi.yaml -o deref.yaml`
- `node -e "const s={openapi:'3.0.0',info:{title:'API',version:'1.0.0'},paths:{}};console.log(JSON.stringify(s,null,2))"`

**Examples:**
- swagger-cli validate openapi.yaml
- swagger-cli bundle openapi.yaml -o bundled.yaml && swagger-cli validate bundled.yaml
- node -e "const s={openapi:'3.0.0',info:{title:'API',version:'1.0.0'},paths:{}};console.log(JSON.stringify(s,null,2))"

### ui-serving
Serve Swagger UI and Redoc locally and in production

**Commands:**
- `npm install -g redoc-cli`
- `redoc-cli serve openapi.yaml`
- `redoc-cli build openapi.yaml -o index.html`
- `npm install swagger-ui-dist`
- `node -e "const d=require('swagger-ui-dist');console.log(d.getAbsoluteFSPath())"`

**Examples:**
- redoc-cli serve openapi.yaml -p 8090
- redoc-cli build openapi.yaml -o index.html
- node -e "const d=require('swagger-ui-dist');console.log(d.getAbsoluteFSPath())"
