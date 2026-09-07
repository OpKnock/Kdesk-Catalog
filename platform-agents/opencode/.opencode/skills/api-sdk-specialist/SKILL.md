---
name: "api-sdk-specialist"
description: "Applies SDK design patterns: configuration objects, typed errors, retry policies, pagination helpers, and package metadata quality with publint. Use when working with sdk design, retry policies or when the user mentions sdk design, retry policies."
---

Applies SDK design patterns: configuration objects, typed errors, retry policies, pagination helpers, and package metadata quality with publint.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm install openapi-fetch`, `npm install p-retry`
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

# API SDK Specialist

SDK design patterns and quality.

## What This Skill Does
- Designs SDK config and error surfaces
- Implements retries and pagination helpers
- Ensures package quality with publint

## When to Use
- SDK refactoring for consistency
- Adding retry behavior
- Preparing SDK releases

## Real Commands

```bash
npm install openapi-fetch
node -e "const api=require('openapi-fetch').createClient({baseUrl:'https://api.example.com',headers:{'X-API-Key':process.env.API_KEY}}); console.log(typeof api.GET)"
npx publint
```

## SDK Pattern

```ts
const client = createClient<paths>({
  baseUrl: process.env.API_URL,
  headers: { 'X-API-Key': process.env.API_KEY },
  fetch: withRetry(fetch, { retries: 3 })
});
```

## Testing
- Test retry behavior with failing mocks
- Validate package exports with publint
- Check types compile for consumers

## Best Practices
- Expose typed errors, not strings
- Keep config objects minimal
- Follow semantic versioning for breaking changes

## Capabilities

### sdk-design
Design consistent SDK configuration and error surfaces

**Parameters:**
- `baseUrl` (string): API base URL
- `headers` (object): Default request headers
- `fetch` (function): Custom fetch implementation

**Commands:**
- `npm install openapi-fetch`
- `node -e "const api=require('openapi-fetch').createClient({baseUrl:'http://localhost:8080',headers:{'X-API-Key':process.env.API_KEY}}); console.log(typeof api.GET)"`
- `node -e "const api=require('openapi-fetch').createClient({baseUrl:'http://localhost:8080'}); api.GET('/users',{params:{query:{page:1}}}).then(r=>console.log(r.data ?? r.error))"`
- `npx publint`

**Examples:**
- createClient sets baseUrl and headers once
- GET returns { data, error } for type-safe handling
- publint validates package.json metadata

### retry-policies
Implement retry and backoff for transient failures

**Commands:**
- `npm install p-retry`
- `node -e "const pRetry=require('p-retry'); const fn=async()=>{const r=await fetch('http://localhost:8080/users'); if(!r.ok) throw new Error('fail'); return r.json()}; pRetry(fn,{retries:3,factor:2}).then(console.log).catch(console.error)"`
- `node -e "const r=require('retry'); console.log(r.operation({retries:3,factor:2}).attempt)"`

**Examples:**
- -cli --help
- -api --help

## References
- [openapi-fetch](https://openapi-ts.dev/openapi-fetch/)
- [publint](https://publint.dev/)
