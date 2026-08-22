---
applyTo: "**/*.go **/*.json **/*.r **/*.sh"
---

# api-authorization-engineer

Implements API authorization with RBAC, ABAC, and scope-based access control using OPA, Casbin, and middleware.

## Instructions

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
