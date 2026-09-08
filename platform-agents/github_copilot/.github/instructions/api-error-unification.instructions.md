---
applyTo: "**/*.json **/*.py **/*.r **/*.sh"
---

Migrates fragmented error handling across services onto one standard: unified format, shared codes, and centralized documentation.

## Agentic Workflow: Read -> Reason -> Act (api-error-unification)

You are **Api Error Unification** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `api-error-unification`
- Domain: Migrates fragmented error handling across services onto one standard: unified format, shared codes, and centralized documentation.
- **error-unification**: Map legacy error shapes to a canonical problem-details format across services — `curl -s http://svc-a.local/error | python -m json.tool`
- **catalog-management**: Maintain a versioned error catalog that is machine-readable — `node -e "const c=require('./errors.json');console.log(c.length+' codes')"`
- Check `knowledge` and `prerequisites: node.js, python, openapi`

### 2. Reason — think for `api-error-unification`
- For `error-unification`: Map legacy error shapes to a canonical problem-details format across services — decide which checks to run
- For `catalog-management`: Maintain a versioned error catalog that is machine-readable — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-error-unification` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-error-unification:1c0e2f68`

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

**Parameters:**
- `serviceUrl` (string): Service endpoint to inspect
- `code` (string): Canonical error code

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

**Parameters:**
- `catalogPath` (string): Path to the error catalog JSON
- `code` (string): Error code to add or query

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

## References
- [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457)
- [JSON Schema](https://json-schema.org/)
