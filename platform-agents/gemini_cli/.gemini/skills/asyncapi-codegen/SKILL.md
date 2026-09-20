---
name: "asyncapi-codegen"
description: "Generates code and docs from AsyncAPI documents with the AsyncAPI CLI, generator templates, and Modelina multi-language models."
---

# Asyncapi Codegen

Generates code and docs from AsyncAPI documents with the AsyncAPI CLI, generator templates, and Modelina multi-language models.

## Instructions

# AsyncAPI Codegen

## What this skill does

Works with AsyncAPI documents end-to-end: validating and linting, generating servers/clients/docs from templates, and producing typed models with Modelina.

## When to use

- An event-driven API needs code generated from its spec
- Validating an AsyncAPI file in CI
- Bootstrapping a Node/Java/Python subscriber from a spec

## Real commands

```bash
# Validate
npx @asyncapi/cli validate asyncapi.yaml
npx @asyncapi/cli lint asyncapi.yaml

# Generate a Node.js app
npx @asyncapi/generator asyncapi.yaml @asyncapi/nodejs-template -o ./generated --force-write

# Generate Java Spring project
npx @asyncapi/generator asyncapi.yaml @asyncapi/java-spring-template -o ./generated

# Generate HTML docs
npx @asyncapi/generator asyncapi.yaml @asyncapi/html-template -o ./docs

# Generate TypeScript models
npx @asyncapi/modelina generate --input asyncapi.yaml --output ./models --language TypeScript
```

## AsyncAPI document (v3)

```yaml
asyncapi: 3.0.0
info:
  title: Order Service
  version: 1.0.0
channels:
  orderCreated:
    address: order.created
    messages:
      OrderCreated:
        payload:
          type: object
          properties:
            id: {type: string}
operations:
  publishOrder:
    action: send
    channel: { $ref: '#/channels/orderCreated' }
```

## Testing

- Validate in CI with npx @asyncapi/cli validate
- Smoke-test generated code with npm install && npm start in the output dir

## Best practices

- Keep the spec the single source of truth
- Re-generate in CI and diff to catch drift
- Use --param server= to select environments

## Capabilities

### validation
Validate and lint AsyncAPI documents.

**Commands:**
- `npx @asyncapi/cli validate asyncapi.yaml`
- `npx @asyncapi/cli lint asyncapi.yaml`
- `npx @asyncapi/cli validate https://raw.githubusercontent.com/asyncapi/spec/master/examples/simple.yml`
- `npx @asyncapi/cli --version`

**Examples:**
- npx @asyncapi/cli validate asyncapi.yaml
- npx @asyncapi/cli lint --ruleset config.json asyncapi.yaml
- npx @asyncapi/cli validate --spec-parser-options '{}' asyncapi.yaml

### generation
Generate server/client code and docs from templates.

**Commands:**
- `npx @asyncapi/generator asyncapi.yaml @asyncapi/nodejs-template -o ./generated --force-write`
- `npx @asyncapi/generator asyncapi.yaml @asyncapi/java-spring-template -o ./generated`
- `npx @asyncapi/generator asyncapi.yaml @asyncapi/python-paho-template -o ./generated`
- `npx @asyncapi/generator asyncapi.yaml @asyncapi/html-template -o ./docs`
- `npx @asyncapi/generator --param server=production asyncapi.yaml @asyncapi/nodejs-template -o ./generated`

**Examples:**
- npx @asyncapi/generator asyncapi.yaml @asyncapi/nodejs-template -o ./out --force-write
- npx @asyncapi/generator --param password=secret asyncapi.yaml @asyncapi/java-spring-template -o ./out
- npx @asyncapi/generator asyncapi.yaml @asyncapi/markdown-template -o ./docs

### modelina
Generate data models for multiple languages from the schema.

**Commands:**
- `npx @asyncapi/modelina generate --input asyncapi.yaml --output ./models --language TypeScript`
- `npx @asyncapi/modelina generate --input asyncapi.yaml --output ./src/main/java --language Java`
- `npx @asyncapi/modelina generate --input asyncapi.yaml --output ./models --language Go`
- `npx @asyncapi/modelina generate --input asyncapi.yaml --output ./models --language Python`

**Examples:**
- npx @asyncapi/modelina generate --input asyncapi.yaml --output ./models --language TypeScript --packageName com.example
- npx @asyncapi/modelina generate --input asyncapi.yaml --output ./models --language Java --type-mapping string=UUID
- npx @asyncapi/modelina generate --input asyncapi.yaml --output ./models --language Python --generate-optional
