Generates Node.js applications from AsyncAPI documents with the nodejs-template, then installs, runs, and tests the generated subscriber.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx @asyncapi/generator asyncapi.yaml @asyncapi/nodejs-templ`, `npx @asyncapi/modelina generate --input asyncapi.yaml --outp`
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