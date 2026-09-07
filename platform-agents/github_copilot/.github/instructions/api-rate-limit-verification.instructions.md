---
applyTo: "**/*.json **/*.r **/*.sh"
---

Verifies rate limiting behavior under load: 429 response testing, header assertions, burst tolerance checks, and k6 scenarios that prove limits hold at scale.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -s -o /dev/null -w '%{http_code}\n' -H 'X-Client-Id: te`, `k6 run --vus 5 --iterations 300 ratelimit-test.js`
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

# API Rate v4 - Limit Testing

Proving rate limits behave under load.

## What This Skill Does
- Verifies exact 429 thresholds per client
- Asserts RateLimit and Retry-After headers
- Proves limits hold under concurrency

## When to Use
- Acceptance tests for new limit configs
- Regression checks after limit refactors
- Documenting observable limit behavior

## Real Commands

```bash
for i in $(seq 1 150); do curl -s -o /dev/null -w '%{http_code}\n' -H 'X-Client-Id: test1' http://localhost:3000/api; done | sort | uniq -c
curl -s -D- -o /dev/null http://localhost:3000/api | grep -iE 'ratelimit|retry-after'
```

## k6 Assertions

```js
const res = http.get('http://localhost:3000/api', { headers: { 'X-Client-Id': __VU } });
if (res.status === 429) {
  check(res, { 'has retry-after': (r) => r.headers['Retry-After'] !== undefined });
}
```

## Testing
- Confirm the burst count matches the configured limit
- Validate header values match window math
- Run with 2x VUs to catch race conditions

## Best Practices
- Test at the exact boundary and one request beyond
- Include a control client that stays under the limit
- Store limit-test scripts with the API source

## Capabilities

### limit-verification
Assert 429s and rate limit headers under controlled load

**Parameters:**
- `client-key` (string): Header or identity that scopes the limit
- `burst` (integer): Requests sent in the verification loop
- `expected-limit` (integer): Limit the implementation should enforce

**Commands:**
- `curl -s -o /dev/null -w '%{http_code}\n' -H 'X-Client-Id: test1' http://localhost:3000/api`
- `for i in $(seq 1 150); do curl -s -o /dev/null -w '%{http_code}\n' -H 'X-Client-Id: test1' http://localhost:3000/api; done | sort | uniq -c`
- `curl -s -D- -o /dev/null http://localhost:3000/api | grep -iE 'ratelimit|retry-after'`
- `ab -n 500 -c 20 http://localhost:3000/api 2>&1 | grep -E 'Non-2xx|Requests per second'`

**Examples:**
- curl loops count how many requests pass before 429s start
- grep -iE 'ratelimit|retry-after' verifies limit headers
- ab reports the non-2xx share under concurrent load

### k6-limit-tests
Script rate limit enforcement tests in k6

**Commands:**
- `k6 run --vus 5 --iterations 300 ratelimit-test.js`
- `k6 run --threshold 'http_req_duration:p(95)<500' ratelimit-test.js`
- `k6 run --summary-export=limit-summary.json ratelimit-test.js`

**Examples:**
- -cli --help
- -api --help

## References
- [RFC 6585 - 429 Too Many Requests](https://www.rfc-editor.org/rfc/rfc6585)
- [k6 HTTP Module](https://grafana.com/docs/k6/latest/javascript-api/k6-http/)
