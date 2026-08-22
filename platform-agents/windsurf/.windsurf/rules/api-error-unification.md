---
trigger: glob
description: "Migrates fragmented error handling across services onto one standard: unified format, shared codes, and centralized documentation."
globs: ["**/*.json", "**/*.py", "**/*.r", "**/*.sh"]
---

# Api Error Unification

Migrates fragmented error handling across services onto one standard: unified format, shared codes, and centralized documentation.

## Instructions

# API Error (Unification & Catalog)

Moves a fleet of services onto one error format with a shared, versioned error catalog.

## When to Use
- Different services return different error shapes
- Clients hand-parse error bodies per service
- Auditors need a machine-readable error inventory

## Real Commands

```bash
# Compare current shapes
curl -s http://svc-a.local/error | python -m json.tool
curl -s http://svc-b.local/error | python -m json.tool

# Validate catalog
node -e "const c=require('./errors.json');console.log(c.length+' codes')"

# Check for duplicate codes
node -e "const c=require('./errors.json');const dup=c.filter((e,i)=>c.findIndex(x=>x.code===e.code)!==i);console.log('dups:',dup.length)"
```

## Migration Order
1. Publish the canonical catalog
2. Add translation middleware (legacy shape in, canonical out)
3. Flip services one at a time
4. Remove translation layer

## Testing
Every service must return the same shape for the same code; assert in CI.

## Best Practices
- Catalog is the source of truth for codes
- Version the catalog; never delete codes, deprecate

## Capabilities

### error-unification
Map legacy error shapes to a canonical problem-details format across services

**Commands:**
- `curl -s http://svc-a.local/error | python -m json.tool`
- `curl -s http://svc-b.local/error | python -m json.tool`
- `node -e "const map={404:{code:'NOT_FOUND',status:404}};console.log(map[404])"`
- `python -c "print({404:{'code':'NOT_FOUND','status':404}})"`
- `curl -s http://localhost:3000/api/errors/catalog | python -m json.tool`

**Examples:**
- curl -s http://svc-a.local/error | python -m json.tool && curl -s http://svc-b.local/error | python -m json.tool
- curl -s http://localhost:3000/api/errors/catalog | python -m json.tool
- node -e "const c=[{old:'NotFoundError',code:'NOT_FOUND',status:404}];console.log(JSON.stringify(c))"

### catalog-management
Maintain a versioned error catalog that is machine-readable

**Commands:**
- `node -e "const c=require('./errors.json');console.log(c.length+' codes')"`
- `python -m json.tool errors.json > errors.pretty.json`
- `node -e "const fs=require('fs');const c=JSON.parse(fs.readFileSync('errors.json'));fs.writeFileSync('errors.json',JSON.stringify(c.concat([{code:'RATE_LIMITED',status:429}]),null,2))"`
- `git diff --stat errors.json`
- `node -e "const c=require('./errors.json');const dup=c.filter((e,i)=>c.findIndex(x=>x.code===e.code)!==i);console.log('dups:',dup.length)"`

**Examples:**
- node -e "const fs=require('fs');const c=JSON.parse(fs.readFileSync('errors.json'));console.log(c.filter(e=>e.status>=500))"
- node -e "const c=require('./errors.json');const dup=c.filter((e,i)=>c.findIndex(x=>x.code===e.code)!==i);console.log('dups:',dup.length)"
- python -m json.tool errors.json > errors.pretty.json && git diff --stat errors.json
