---
applyTo: "**/*.json **/*.r **/*.sh"
---

General-purpose API mocking: mountebank imposters, response templating, request matching, and delay/fault simulation.

## Agentic Workflow: Read -> Reason -> Act (mocking)

You are **Mocking** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `mocking`
- Domain: General-purpose API mocking: mountebank imposters, response templating, request matching, and delay/fault simulation.
- **api-mocking**: Create mock HTTP services with mountebank, add behavioral stubs, and simulate latency or faults. — `mb start --port 2525`
- Check `knowledge` and `prerequisites: mb`

### 2. Reason — think for `mocking`
- For `api-mocking`: Create mock HTTP services with mountebank, add behavioral stubs, and simulate latency or faults. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `mocking` tools
- Tools: `Glob`, `Grep`, `Read`, `Mb`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `mocking:24815063`

# Mocking

Mock HTTP services isolate your application from dependencies during development and testing.

## What this skill does

- Boots mountebank and registers imposter services
- Matches requests with predicates and returns templated responses
- Simulates latency, errors and flaky behavior

## When to use

- Testing against a third-party API that is expensive or flaky
- Reproducing timeouts and 5xx for resilience work
- Contract tests without spinning up real dependencies

## Real commands

```bash
# Start mountebank control plane
mb start --port 2525

# Register an imposter from file
curl -X POST http://localhost:2525/imposters -d @imposter.json

# Register inline: HTTP on 3000 returning 200 "ok"
curl -X POST -H "Content-Type: application/json" \
  -d '{"port":3000,"protocol":"http","stubs":[{"responses":[{"is":{"statusCode":200,"body":"ok"}}]}]}' \
  http://localhost:2525/imposters

# Inspect requests captured by the imposter
curl http://localhost:2525/imposters/3000

# Remove the imposter
curl -X DELETE http://localhost:2525/imposters/3000
```

## imposter.json with predicate + delay

```json
{
  "port": 3000,
  "protocol": "http",
  "stubs": [{
    "predicates": [{ "equals": { "method": "GET", "path": "/users/1" } }],
    "responses": [{ "is": { "statusCode": 200, "body": "{\"id\":1}" }, "behaviors": [{ "wait": 2000 }] }]
  }]
}
```

## Best practices

- Give every stub a distinct `name` for debuggability
- Prefer deterministic responses in CI; use injection only locally
- Clean up imposters in teardown (`mb stop`)

## Capabilities

### api-mocking
Create mock HTTP services with mountebank, add behavioral stubs, and simulate latency or faults.

**Parameters:**
- `port` (integer): Port the mock imposter listens on
- `protocol` (string): http, https, tcp or smtp
- `latency` (integer): Milliseconds of response delay

**Commands:**
- `mb start --port 2525`
- `curl -X POST http://localhost:2525/imposters -d @imposter.json`
- `curl -X POST -H "Content-Type: application/json" -d '{"port":3000,"protocol":"http","stubs":[{"responses":[{"is":{"statusCode":200,"body":"ok"}}]}]}' http://localhost:2525/imposters`
- `curl http://localhost:2525/imposters`
- `curl -X DELETE http://localhost:2525/imposters/3000`

**Examples:**
- mb start --port 2525 --allowInjection
- curl -X POST http://localhost:2525/imposters -d @imposter.json
- curl http://localhost:2525/imposters/3000

## References
- [Mountebank Docs](https://www.mbtest.org/docs/)
- [Mock Service Worker](https://mswjs.io/docs/)
