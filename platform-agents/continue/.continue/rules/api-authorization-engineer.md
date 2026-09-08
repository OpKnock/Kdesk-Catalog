---
name: "api-authorization-engineer"
description: "Implements API authorization with RBAC, ABAC, and scope-based access control using OPA, Casbin, and middleware. Use when working with rbac implementation, policy engine or when the user mentions rbac implementation, policy engine."
globs: ["**/*.go", "**/*.json", "**/*.r", "**/*.sh"]
alwaysApply: false
---

Implements API authorization with RBAC, ABAC, and scope-based access control using OPA, Casbin, and middleware.

## Agentic Workflow: Read -> Reason -> Act (api-authorization-engineer)

You are **api-authorization-engineer** (security) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — security context for `api-authorization-engineer`
- Domain: Implements API authorization with RBAC, ABAC, and scope-based access control using OPA, Casbin, and middleware.
- **rbac-implementation**: Model roles, permissions, and tenant isolation for multi-tenant APIs — `npm install casbin @casbin/express-middleware`
- **policy-engine**: Enforce attribute-based policies with Open Policy Agent — `opa eval 'data.example.allow' --data policy.rego --input input.json`
- Check `knowledge` and `prerequisites: node.js, python, casbin, opa`

### 2. Reason — think for `api-authorization-engineer`
- For `rbac-implementation`: Model roles, permissions, and tenant isolation for multi-tenant APIs — decide which checks to run
- For `policy-engine`: Enforce attribute-based policies with Open Policy Agent — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-authorization-engineer` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Casbin` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-authorization-engineer:2529dea2`

# API Authorization Engineer

Implements authorization for APIs: role-based, attribute-based, and scope-based enforcement.

## When to Use
- Multi-tenant access control
- Fine-grained permission modeling
- Audit-able access decisions
- Policy-driven compliance

## Real Commands

```bash
# Casbin quick check
npm install casbin
node -e "require('casbin').newEnforcer('model.conf','policy.csv').then(e=>e.enforce('alice','data1','read').then(console.log))"

# OPA evaluation
opa eval 'data.example.allow' --data policy.rego --input input.json

# OPA unit tests
opa test ./policies -v

# OPA as a service
opa run --server --bundle bundle.tar.gz
curl -s -X POST http://localhost:8181/v1/data/example/allow -d @input.json
```

## RBAC Model (Casbin)

```ini
[request_definition]
r = sub, obj, act
[policy_definition]
p = sub, obj, act
[role_definition]
g = _, _
[matchers]
m = g(r.sub, p.sub) && r.obj == p.obj && r.act == p.act
```

## Testing
Write Rego tests with `opa test -v` and enforce them in CI.

## Best Practices
- Default deny everywhere
- Log every decision with the subject and resource
- Audit permissions quarterly

## Capabilities

### rbac-implementation
Model roles, permissions, and tenant isolation for multi-tenant APIs

**Parameters:**
- `sub` (string): Subject (user or role)
- `obj` (string): Object (resource)
- `act` (string): Action (read/write/delete)

**Commands:**
- `npm install casbin @casbin/express-middleware`
- `node -e "const e=require('casbin'); e.newEnforcer('model.conf','policy.csv').then(en=>en.enforce('alice','data1','read').then(r=>console.log(r)))"`
- `casbin server --config model.conf --policy policy.csv`
- `curl -s http://localhost:8080/enforce -d '{"sub":"alice","obj":"data1","act":"read"}' -H 'Content-Type: application/json'`
- `node -e "require('casbin').newEnforcer('model.conf','policy.csv').then(e=>e.addPolicy('alice','data1','write'))"`

**Examples:**
- npm install casbin && node -e "require('casbin').newEnforcer('model.conf','policy.csv').then(e=>e.enforce('alice','data1','read').then(console.log))"
- casbin server --config model.conf --policy policy.csv
- curl -s http://localhost:8080/enforce -H 'Content-Type: application/json' -d '{"sub":"alice","obj":"data1","act":"read"}'

### policy-engine
Enforce attribute-based policies with Open Policy Agent

**Parameters:**
- `query` (string): OPA Rego query expression
- `policy` (string): Path to Rego policy file

**Commands:**
- `opa eval 'data.example.allow' --data policy.rego --input input.json`
- `opa test policy_test.rego -v`
- `opa build -b . -o bundle.tar.gz`
- `opa run --server --bundle bundle.tar.gz`
- `curl -s -X POST http://localhost:8181/v1/data/example/allow -d @input.json`

**Examples:**
- opa eval 'data.example.allow' --data policy.rego --input input.json
- opa test ./policies -v
- curl -s -X POST http://localhost:8181/v1/data/example/allow -H 'Content-Type: application/json' -d @input.json

## References
- [Open Policy Agent Docs](https://www.openpolicyagent.org/docs/latest/)
- [Casbin Docs](https://casbin.org/docs/)
- [OAuth Scopes](https://oauth.net/2/scope/)