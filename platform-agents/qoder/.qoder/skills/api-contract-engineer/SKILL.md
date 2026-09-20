---
name: "api-contract-engineer"
description: "Hands-on implementation of contract testing: Pact consumer tests, provider verification, and schema validation wired into CI. Use when working with pact implementation, schema validation or when the user mentions pact implementation, schema validation."
license: "MIT"
compatibility: "Requires pact, openapi, node.js, python, postman."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "testing"}
allowed-tools: "Glob Grep Read Bash(node:*) Bash(npm:*) Bash(npx:*) Bash(pip:*)"
---

Hands-on implementation of contract testing: Pact consumer tests, provider verification, and schema validation wired into CI.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm install @pact-foundation/pact`, `npm install ajv`
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

# API Contract Engineer

Implements contract tests that catch breaking API changes before they reach production.

## When to Use
- Consumer and provider teams move fast
- Breaking changes keep slipping through
- Third-party APIs need guards

## Real Commands

```bash
# Install
npm install @pact-foundation/pact

# Run consumer tests
npx jest --testMatch '**/pact/*.test.js'

# Publish contracts
npx pact-broker publish ./pacts --consumer-version 1.0.0 --broker-base-url http://localhost:9292

# Provider verification
npm run test:provider

# Validate spec parses
node -e "const P=require('@apidevtools/swagger-parser');P.validate('openapi.yaml').then(()=>console.log('valid'))"
```

## Provider State
Set up provider states so verification runs against known fixtures.

## Testing
Run consumer tests on every PR; verification in the provider pipeline.

## Best Practices
- Publish contracts with unique versions
- Gate deploys with can-i-deploy
- Keep pacts small and readable

## Capabilities

### pact-implementation
Write and run Pact consumer and provider tests in Node and Python

**Parameters:**
- `consumer` (string): Consumer app name
- `provider` (string): Provider app name
- `version` (string): Consumer version

**Commands:**
- `npm install @pact-foundation/pact`
- `npx jest --testMatch '**/pact/*.test.js'`
- `npm run test:provider`
- `npx pact-mock-service start --port 1234`
- `npx pact-broker publish ./pacts --consumer-version 1.0.0 --broker-base-url http://localhost:9292`

**Examples:**
- npx jest --testMatch '**/pact/*.test.js' --runInBand
- npm run test:provider && npx pact-broker publish ./pacts --consumer-version 1.0.0
- npx pact-mock-service start --port 1234 --pact-dir ./pacts

### schema-validation
Validate live API responses against OpenAPI-derived JSON Schemas in tests

**Parameters:**
- `spec` (string): OpenAPI spec path
- `response` (string): Response JSON to validate

**Commands:**
- `npm install ajv`
- `npm install @apidevtools/swagger-parser`
- `node -e "const P=require('@apidevtools/swagger-parser');P.validate('openapi.yaml').then(()=>console.log('valid')).catch(e=>console.log(e.message))"`
- `node -e "const Ajv=require('ajv');const a=new Ajv();console.log(a.validate({type:'object',additionalProperties:false,required:['id']},{id:1,x:2})===false?'rejected':'passed')"`
- `pip install openapi-schema-validator && python -c "from openapi_schema_validator import validate;print('ok')"`

**Examples:**
- node -e "const P=require('@apidevtools/swagger-parser');P.validate('openapi.yaml').then(()=>console.log('valid'))"
- node -e "const Ajv=require('ajv');const a=new Ajv();console.log(a.validate({type:'object',required:['id']},{id:1}))"
- python -c "from openapi_schema_validator import validate;validate({'id':1},{'type':'object','required':['id']});print('ok')"

## References
- [Pact JS](https://docs.pact.io/implementation_guides/javascript/)
- [Pact Broker](https://docs.pact.io/pact_broker/)
- [swagger-parser](https://apitools.dev/swagger-parser/)
