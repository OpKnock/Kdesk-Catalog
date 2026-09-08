---
name: "asyncapi-nodejs"
description: "Generates Node.js applications from AsyncAPI documents with the nodejs-template, then installs, runs, and tests the generated subscriber. Use when working with node generation, ts models, api or when the user mentions node generation, ts models, api."
type: knowledge
triggers: ["asyncapi-nodejs", "node-generation", "ts-models"]
---

Generates Node.js applications from AsyncAPI documents with the nodejs-template, then installs, runs, and tests the generated subscriber.

## Agentic Workflow: Read -> Reason -> Act (asyncapi-nodejs)

You are **Asyncapi Nodejs** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `asyncapi-nodejs`
- Domain: Generates Node.js applications from AsyncAPI documents with the nodejs-template, then installs, runs, and tests the generated subscriber.
- **node-generation**: Generate a Node.js async API app from the spec. — `npx @asyncapi/generator asyncapi.yaml @asyncapi/nodejs-template -o ./generated -`
- **ts-models**: Generate TypeScript models from the schema with Modelina. — `npx @asyncapi/modelina generate --input asyncapi.yaml --output ./generated/src/m`
- Check `knowledge` and `prerequisites: node, npm, npx`

### 2. Reason — think for `asyncapi-nodejs`
- For `node-generation`: Generate a Node.js async API app from the spec. — decide which checks to run
- For `ts-models`: Generate TypeScript models from the schema with Modelina. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `asyncapi-nodejs` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `asyncapi-nodejs:5958e564`

# AsyncAPI Node.js

## What this skill does

Generates a Node.js event-driven application from an AsyncAPI document using the nodejs-template: scaffolding, dependency install, generated handlers, and TypeScript models via Modelina.

## When to use

- Bootstrapping a Node.js Kafka/MQTT/AMQP subscriber or publisher
- Generating typed message models for a TS codebase
- Prototyping an event-driven service from a spec

## Real commands

```bash
# Generate the app
npx @asyncapi/generator asyncapi.yaml @asyncapi/nodejs-template -o ./generated --force-write

# Install dependencies
npm install --prefix ./generated

# Run
npm start --prefix ./generated

# Tests
npm test --prefix ./generated

# TypeScript models
npx @asyncapi/modelina generate --input asyncapi.yaml --output ./generated/src/models --language TypeScript
npm run build --prefix ./generated
```

## Generated handlers

The template creates handler stubs per channel operation (e.g. handleOrderCreated) where you fill in business logic.

## Testing

- npm test --prefix ./generated runs scaffolded unit tests
- Integration: start a local broker (docker run -p 9092:9092 apache/kafka), publish a sample message, confirm the handler logs it

## Best practices

- Use --param server=... to select the broker environment
- Regenerate in CI and git diff --exit-code to catch drift
- Keep business logic in separate modules, not inside generated handlers

## Capabilities

### node-generation
Generate a Node.js async API app from the spec.

**Parameters:**
- `output` (string): Output directory
- `param` (string): Template params like server=production

**Commands:**
- `npx @asyncapi/generator asyncapi.yaml @asyncapi/nodejs-template -o ./generated --force-write`
- `npm install --prefix ./generated`
- `npm start --prefix ./generated`
- `npm test --prefix ./generated`
- `node -e "const p=require('./generated/package.json'); console.log(p.scripts)"`

**Examples:**
- npx @asyncapi/generator asyncapi.yaml @asyncapi/nodejs-template -o ./generated --force-write --param server=development
- npm install --prefix ./generated && npm start --prefix ./generated
- npm test --prefix ./generated

### ts-models
Generate TypeScript models from the schema with Modelina.

**Parameters:**
- `model_type` (string): class or interface for TypeScript models
- `output` (string): Models output directory

**Commands:**
- `npx @asyncapi/modelina generate --input asyncapi.yaml --output ./generated/src/models --language TypeScript`
- `npm run build --prefix ./generated`
- `npm run lint --prefix ./generated`
- `npx tsc --noEmit --project ./generated`

**Examples:**
- npx @asyncapi/modelina generate --input asyncapi.yaml --output ./src/models --language TypeScript --model-type interface
- npm run build --prefix ./generated
- npx tsc --noEmit --project ./generated

## References
- [Node.js Template](https://github.com/asyncapi/nodejs-template)
- [Modelina TypeScript](https://www.asyncapi.com/docs/tools/modelina/languages/TypeScript)
- [AsyncAPI Tutorials](https://www.asyncapi.com/docs/tutorials/getting-started/event-driven-architectures)
