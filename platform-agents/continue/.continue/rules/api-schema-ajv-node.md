---
name: "Api Schema Ajv Node"
description: "Uses JSON Schema in Node.js validation pipelines: ajv with formats, custom keywords, schema compilation caching, and request validation middleware. Use when working with ajv node, request validation or when the user mentions ajv node, request validation."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
alwaysApply: false
---

Uses JSON Schema in Node.js validation pipelines: ajv with formats, custom keywords, schema compilation caching, and request validation middleware.

## Agentic Workflow: Read -> Reason -> Act (api-schema-ajv-node)

You are **Api Schema Ajv Node** (data) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — data context for `api-schema-ajv-node`
- Domain: Uses JSON Schema in Node.js validation pipelines: ajv with formats, custom keywords, schema compilation caching, and request validation middleware.
- **ajv-node**: Compile and use ajv validators in Node — `npm install ajv ajv-formats`
- **request-validation**: Validate request bodies in middleware — `node -e "const Ajv=require('ajv'); const v=new Ajv().compile({type:'object',addi`
- Check `knowledge` and `prerequisites: openapi, json-schema, node.js, python`

### 2. Reason — think for `api-schema-ajv-node`
- For `ajv-node`: Compile and use ajv validators in Node — decide which checks to run
- For `request-validation`: Validate request bodies in middleware — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-schema-ajv-node` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-schema-ajv-node:a7772fe6`

# API Schema v2 - Node Validation

JSON Schema validation in Node.js.

## What This Skill Does
- Validates payloads with ajv
- Extends validation with formats and keywords
- Integrates into request middleware

## When to Use
- Node API request validation
- Validating external data
- Shared schema modules

## Real Commands

```bash
npm install ajv ajv-formats
node -e "const Ajv=require('ajv'); const addFormats=require('ajv-formats'); const a=new Ajv({allErrors:true}); addFormats(a); const v=a.compile({type:'object',properties:{email:{type:'string',format:'email'}},required:['email']}); console.log(v({email:'a@b.co'}))"
```

## Middleware Pattern

```js
const validate = ajv.compile(userSchema);
app.post('/api/users', (req, res) => {
  if (!validate(req.body)) return res.status(400).json(validate.errors);
  res.status(201).end();
});
```

## Testing
- Test valid and invalid fixtures
- Verify 400 responses carry error details
- Benchmark compiled validator performance

## Best Practices
- Compile validators once at startup
- Use additionalProperties:false for strict DTOs
- Keep schemas versioned and shared

## Capabilities

### ajv-node
Compile and use ajv validators in Node

**Parameters:**
- `schema` (object): Schema object
- `data` (object): Payload to validate
- `allErrors` (boolean): Report all errors

**Commands:**
- `npm install ajv ajv-formats`
- `node -e "const Ajv=require('ajv'); const addFormats=require('ajv-formats'); const a=new Ajv({allErrors:true}); addFormats(a); const v=a.compile({type:'object',properties:{email:{type:'string',format:'email'}},required:['email']}); console.log(v({email:'a@b.co'}), JSON.stringify(v.errors))"`
- `node -e "const Ajv=require('ajv'); const a=new Ajv(); a.addKeyword({keyword:'even',validate:(s,v)=>v%2===0}); const v=a.compile({type:'integer',even:true}); console.log(v(2), v(3))"`
- `node -e "const Ajv=require('ajv'); const a=new Ajv(); console.log(a.compile({type:'object'}).schema)"`

**Examples:**
- new Ajv({allErrors:true}) reports all violations
- addKeyword defines custom validation keywords
- compile once, reuse for request validation

### request-validation
Validate request bodies in middleware

**Commands:**
- `node -e "const Ajv=require('ajv'); const v=new Ajv().compile({type:'object',additionalProperties:false}); console.log(v({}), v({extra:1}))"`
- `curl -s -X POST http://localhost:3000/api/users -H 'Content-Type: application/json' -d '{"email":"bad"}' -o /dev/null -w '%{http_code}\n'`
- `curl -s -X POST http://localhost:3000/api/users -H 'Content-Type: application/json' -d '{"email":"ok@x.co"}' -o /dev/null -w '%{http_code}\n'`

**Examples:**
- -cli --help
- -api --help

## References
- [Ajv Guide](https://ajv.js.org/guide/getting-started.html)
- [Ajv Keywords](https://ajv.js.org/docs/guide/custom-keywords.html)