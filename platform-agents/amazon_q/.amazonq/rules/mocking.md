General-purpose API mocking: mountebank imposters, response templating, request matching, and delay/fault simulation.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `mb start --port 2525`
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