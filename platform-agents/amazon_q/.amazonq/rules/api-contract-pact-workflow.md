Designs consumer-driven contract testing setups: Pact workflows, contract publishing, and provider verification pipelines.

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

**Parameters:**
- `broker` (string): Pact Broker URL
- `participant` (string): Consumer or provider name

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

**Parameters:**
- `schema` (string): JSON Schema to validate against
- `data` (string): Response data

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

## References
- [Pact Docs](https://docs.pact.io/)
- [Pact Broker CLI](https://docs.pact.io/pact_broker/client_cli)
- [AJV](https://ajv.js.org/)