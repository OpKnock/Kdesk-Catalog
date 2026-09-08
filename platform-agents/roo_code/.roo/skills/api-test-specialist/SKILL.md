---
name: "api-test-specialist"
description: "Builds API test suites with Postman and Newman: collections, environments, assertions, data-driven iterations, and CI execution with reporters. Use when working with newman execution, postman assertions or when the user mentions newman execution, postman assertions."
license: "MIT"
compatibility: "Requires jest, pytest, postman, newman, supertest. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "testing"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(newman:*) Bash(node:*) Bash(npm:*) Bash(npx:*)"
---

Builds API test suites with Postman and Newman: collections, environments, assertions, data-driven iterations, and CI execution with reporters.

## Agentic Workflow: Read -> Reason -> Act (api-test-specialist)

You are **api-test-specialist** (testing) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — testing context for `api-test-specialist`
- Domain: Builds API test suites with Postman and Newman: collections, environments, assertions, data-driven iterations, and CI execution with reporters.
- **newman-execution**: Run Postman collections in CI — `npm install -g newman`
- **postman-assertions**: Write response assertions in collections — `node -e "const c=require('./collection.json'); const t=c.item[0].event[0].script`
- Check `knowledge` and `prerequisites: jest, pytest, postman`

### 2. Reason — think for `api-test-specialist`
- For `newman-execution`: Run Postman collections in CI — decide which checks to run
- For `postman-assertions`: Write response assertions in collections — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-test-specialist` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Newman` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-test-specialist:58cde01e`

# API Test Specialist

Postman/Newman API testing.

## What This Skill Does
- Organizes tests into collections
- Runs them in CI with newman
- Reports results as JSON/HTML

## When to Use
- Quick API smoke suites
- Team testing without code
- Data-driven endpoint checks

## Real Commands

```bash
npm install -g newman
newman run collection.json -e production.postman_environment.json -r cli,json --reporter-json-export results.json
newman run collection.json --folder "auth" --iteration-data data.csv
```

## Assertion Pattern

```js
pm.test("status is 200", () => {
  pm.response.to.have.status(200);
});
pm.test("has data", () => {
  const json = pm.response.json();
  pm.expect(json.data).to.be.an("array");
});
```

## Testing
- Run the full suite pre-merge
- Use data files for parameterized cases
- Publish JSON results to dashboards


## Best Practices
- Version collections in git
- Store secrets in environments
- Keep assertions granular

## Capabilities

### newman-execution
Run Postman collections in CI

**Parameters:**
- `collection` (string): Collection file path
- `environment` (string): Environment JSON
- `reporters` (string): cli, json, html, junit

**Commands:**
- `npm install -g newman`
- `newman run collection.json -e production.postman_environment.json -r cli,json --reporter-json-export results.json`
- `newman run collection.json --folder "auth" --iteration-data data.csv --reporters cli`
- `newman run collection.json -n 3 --delay-request 100`
- `newman run collection.json --env-var baseUrl=http://localhost:3000`

**Examples:**
- newman -e production selects environment variables
- --folder runs a subset of requests
- --iteration-data drives data-driven tests

### postman-assertions
Write response assertions in collections

**Commands:**
- `node -e "const c=require('./collection.json'); const t=c.item[0].event[0].script.exec.join('\n'); console.log(t.includes('pm.test'))"`
- `curl -s https://postman-echo.com/get?q=1 -o /dev/null -w '%{http_code}\n'`
- `npx postman-to-openapi collection.json -o openapi.yaml`

**Examples:**
- -cli --help
- -api --help

## References
- [Newman CLI](https://learning.postman.com/docs/collections/running-collections/using-newman-cli/)
- [Postman Tests](https://learning.postman.com/docs/writing-scripts/test-scripts/)
