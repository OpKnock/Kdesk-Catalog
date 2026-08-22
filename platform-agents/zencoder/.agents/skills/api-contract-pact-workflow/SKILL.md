---
name: "api-contract-pact-workflow"
description: "Designs consumer-driven contract testing setups: Pact workflows, contract publishing, and provider verification pipelines."
---

# Api Contract Pact Workflow

Designs consumer-driven contract testing setups: Pact workflows, contract publishing, and provider verification pipelines.

## Instructions

# API Contract (Design)

Designs consumer-driven contract testing: who writes what, where contracts live, and how verification gates releases.

## When to Use
- Microservices with many consumers
- Preventing breaking changes between teams
- Contract-first development

## Real Commands

```bash
# Start a local Pact Broker
brew install pact_broker

# Publish contracts
npx pact-broker publish ./pacts -a 1.0.0 -b http://localhost:9292

# Gate deploys
npx pact-broker can-i-deploy --pacticipant consumer -a 1.0.0 --to prod -b http://localhost:9292

# Schema validation
npm install ajv
node -e "const Ajv=require('ajv');const a=new Ajv();console.log(a.validate({type:'object',required:['id']},{id:1}))"
```

## Design Decisions
- Consumer tests define the contract
- Provider verifies all consumer contracts in CI
- Broker is the integration point

## Testing
Run `can-i-deploy` as the final gate in every release pipeline.

## Best Practices
- One contract version per app version
- Tag prod versions in the broker
- Keep contracts small and focused

## Capabilities

### pact-workflow
Write consumer tests, publish contracts, and verify providers against them

**Commands:**
- `npm install @pact-foundation/pact`
- `npx pact-broker publish ./pacts -a 1.0.0 -b http://localhost:9292`
- `npx pact-broker can-i-deploy --pacticipant consumer -a 1.0.0 --to prod -b http://localhost:9292`
- `npm install @pact-foundation/pact-node`
- `npx pact-broker list-latest-pacticipant-versions consumer -b http://localhost:9292`

**Examples:**
- npx pact-broker publish ./pacts -a 1.0.0 -b http://localhost:9292
- npx pact-broker can-i-deploy --pacticipant consumer -a 1.0.0 --to prod -b http://localhost:9292
- npx pact-broker list-latest-pacticipant-versions consumer -b http://localhost:9292

### schema-validation
Validate API responses against JSON Schema from OpenAPI

**Commands:**
- `npm install ajv`
- `node -e "const Ajv=require('ajv');const a=new Ajv();console.log(a.validate({type:'object',required:['id']},{id:1}))"`
- `npm install @apidevtools/json-schema-ref-parser`
- `python -m pip install jsonschema && python -c "import jsonschema;print(jsonschema.validate({'id':1},{'type':'object','required':['id']}))"`
- `node -e "const Ajv=require('ajv');const a=new Ajv();const v=a.compile({type:'object',required:['id']});try{v({x:1})}catch(e){console.log(e.message)}"`

**Examples:**
- node -e "const Ajv=require('ajv');const a=new Ajv();console.log(a.validate({type:'object',required:['id']},{id:1}))"
- python -c "import jsonschema;jsonschema.validate({'x':1},{'type':'object','required':['id']})" 2>&1 | tail -1
- node -e "const Ajv=require('ajv');const a=new Ajv();console.log(a.validate({type:'number',minimum:0},-1)===false?'rejected':'passed')"
