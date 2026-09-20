---
applyTo: "**/*.json **/*.py **/*.r **/*.sh"
---

Implements gateway architecture patterns: BFF composition, protocol translation, routing, and centralized security across clients.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm init -y && npm install express node-fetch`, `npm install @graphql-tools/executor-http`
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

# API Gateway Patterns

Applies gateway architectural patterns: BFF, composition, translation, and edge security.

## When to Use
- Multiple clients need different shapes
- Services speak different protocols
- Centralizing cross-cutting concerns

## Real Commands

```bash
# BFF stub
node -e "const express=require('express');const app=express();app.get('/api/home',(req,res)=>res.json({users:[],orders:[]}));app.listen(3000)"
curl -s http://localhost:3000/api/home | python -m json.tool

# Compose upstreams
node -e "const fetch=require('node-fetch');Promise.all([fetch('http://localhost:3100/users'),fetch('http://localhost:3200/orders')]).then(rs=>Promise.all(rs.map(r=>r.json()))).then(console.log)"

# GraphQL translation check
node -e "const {buildSchema,graphql}=require('graphql');const s=buildSchema('type Query{hello:String}');graphql(s,'{hello}').then(r=>console.log(r))"
```

## Pattern Selection
- One client type: plain gateway routing
- Many client types: BFF per client
- Mixed protocols: translation layer

## Testing
Load test the composed route and confirm p95 stays within budget.

## Best Practices
- Keep BFFs thin; business logic stays in services
- Cache composed responses aggressively

## Capabilities

### bff-composition
Build a Backend-for-Frontend that composes multiple services into client-shaped responses

**Parameters:**
- `route` (string): Composed route path
- `services` (string): Comma-separated upstream services

**Commands:**
- `npm init -y && npm install express node-fetch`
- `node -e "const express=require('express');const app=express();app.get('/api/home',(req,res)=>res.json({users:[],orders:[]}));app.listen(3000,()=>console.log('bff on 3000'))"`
- `curl -s http://localhost:3000/api/home | python -m json.tool`
- `node -e "const fetch=require('node-fetch');Promise.all([fetch('http://localhost:3100/users'),fetch('http://localhost:3200/orders')]).then(rs=>Promise.all(rs.map(r=>r.json()))).then(console.log)"`
- `curl -s -o /dev/null -w '%{http_code} %{time_total}s\n' http://localhost:3000/api/home`

**Examples:**
- node -e "const express=require('express');const app=express();app.get('/api/home',(req,res)=>res.json({users:[],orders:[]}));app.listen(3000)"
- curl -s http://localhost:3000/api/home | python -m json.tool
- curl -s -o /dev/null -w '%{http_code} %{time_total}s\n' http://localhost:3000/api/home

### protocol-translation
Translate between REST, GraphQL, and gRPC at the edge

**Parameters:**
- `from` (string): Source protocol
- `to` (string): Target protocol

**Commands:**
- `npm install @graphql-tools/executor-http`
- `node -e "console.log('grpc_health_probe -addr=localhost:50051')"`
- `curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"{ hello }"}'`
- `node -e "const {buildSchema,graphql}=require('graphql');const s=buildSchema('type Query{hello:String}');graphql(s,'{hello}').then(r=>console.log(r))"`
- `curl -s http://localhost:3000/api/legacy -o /dev/null -w '%{http_code}'`

**Examples:**
- node -e "const {buildSchema,graphql}=require('graphql');const s=buildSchema('type Query{hello:String}');graphql(s,'{hello}').then(r=>console.log(r))"
- curl -s -X POST http://localhost:4000/graphql -H 'Content-Type: application/json' -d '{"query":"{ hello }"}'
- npm install @graphql-tools/executor-http

## References
- [BFF Pattern](https://samnewman.io/patterns/architectural/bff/)
- [API Gateway Pattern](https://microservices.io/patterns/apigateway.html)
