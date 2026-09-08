---
trigger: glob
description: "Deep expertise in API documentation quality: spec consistency, example correctness, and docs-as-code workflows. Use when working with doc quality, example verification or when the user mentions doc quality, example verification."
globs: ["**/*.json", "**/*.py", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

Deep expertise in API documentation quality: spec consistency, example correctness, and docs-as-code workflows.

## Agentic Workflow: Read -> Reason -> Act (api-doc-specialist)

You are **api-doc-specialist** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `api-doc-specialist`
- Domain: Deep expertise in API documentation quality: spec consistency, example correctness, and docs-as-code workflows.
- **doc-quality**: Lint specs for documentation completeness: descriptions, examples, and summaries — `npx @stoplight/spectral-cli lint -r doc-rules.yaml openapi.yaml`
- **example-verification**: Verify every documented example is correct with a mock server — `prism mock openapi.yaml -p 4010`
- Check `knowledge` and `prerequisites: swagger-cli, redoc-cli, openapi-generator`

### 2. Reason — think for `api-doc-specialist`
- For `doc-quality`: Lint specs for documentation completeness: descriptions, examples, and summaries — decide which checks to run
- For `example-verification`: Verify every documented example is correct with a mock server — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-doc-specialist` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx`, `Redocly` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-doc-specialist:67461f57`

# API Doc Specialist

Audits and improves the quality of API documentation itself.

## When to Use
- Docs exist but are thin or wrong
- Examples fail against the real API
- Consistent docs across many endpoints

## Real Commands

```bash
# Completeness linting
npx @stoplight/spectral-cli lint -r doc-rules.yaml openapi.yaml
redocly lint openapi.yaml --extends=recommended

# Find missing summaries
node -e "const spec=require('./openapi.json');Object.entries(spec.paths).forEach(([p,ops])=>Object.entries(ops).filter(([m])=>['get','post','put','patch','delete'].includes(m)).forEach(([m,o])=>console.log(p,o.summary?'ok':'MISSING SUMMARY')))"

# Verify examples against mock
prism mock openapi.yaml -p 4010
curl -s http://localhost:4010/api/products | python -m json.tool
```

## Quality Checklist
- Every operation: summary, description, examples
- Every parameter: example
- Every error: documented schema

## Testing
Run prism mock and click through generated docs.

## Best Practices
- Enforce doc rules in CI
- Ship examples that are copy-paste runnable

## Capabilities

### doc-quality
Lint specs for documentation completeness: descriptions, examples, and summaries

**Parameters:**
- `spec` (string): OpenAPI spec path
- `ruleset` (string): Doc-focused ruleset

**Commands:**
- `npx @stoplight/spectral-cli lint -r doc-rules.yaml openapi.yaml`
- `redocly lint openapi.yaml --extends=recommended`
- `node -e "const spec=require('./openapi.json');Object.entries(spec.paths).forEach(([p,ops])=>Object.entries(ops).filter(([m])=>['get','post','put','patch','delete'].includes(m)).forEach(([m,o])=>console.log(p,m,o.summary?'has summary':'MISSING SUMMARY')))"`
- `python -c "import json;s=json.load(open('openapi.json'));print(len(s.get('paths',{}))) "`
- `npx @stoplight/spectral-cli lint -r doc-rules.yaml --format json openapi.yaml > doc-report.json`

**Examples:**
- node -e "const spec=require('./openapi.json');Object.entries(spec.paths).forEach(([p,ops])=>Object.entries(ops).filter(([m])=>['get','post','put','patch','delete'].includes(m)).forEach(([m,o])=>console.log(p,o.summary?'ok':'MISSING SUMMARY')))"
- redocly lint openapi.yaml --extends=recommended
- npx @stoplight/spectral-cli lint -r doc-rules.yaml --format json openapi.yaml > doc-report.json

### example-verification
Verify every documented example is correct with a mock server

**Parameters:**
- `spec` (string): OpenAPI spec path
- `port` (string): Mock server port

**Commands:**
- `prism mock openapi.yaml -p 4010`
- `curl -s http://localhost:4010/api/products | python -m json.tool`
- `curl -s -o /dev/null -w '%{http_code}' http://localhost:4010/api/products/1`
- `npm install @stoplight/prism-cli`
- `prism proxy http://localhost:3000/api http://localhost:4010`

**Examples:**
- prism mock openapi.yaml -p 4010 && curl -s http://localhost:4010/api/products | python -m json.tool
- prism proxy http://localhost:3000/api http://localhost:4010
- curl -s -o /dev/null -w 'status=%{http_code}\n' http://localhost:4010/api/products/1

## References
- [Redocly Lint Rules](https://redocly.com/docs/rules/)
- [Prism](https://meta.stoplight.io/docs/prism)
