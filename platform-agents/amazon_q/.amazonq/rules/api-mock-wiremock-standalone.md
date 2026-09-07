Builds stateful mock APIs with WireMock standalone: stub mappings via Admin API, request matching, record-and-playback proxying, and stateful scenarios.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `java -jar wiremock-standalone-3.9.1.jar --port 8080`, `curl -s -X POST http://localhost:8080/__admin/recordings/sta`
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

# API Mock v3 - WireMock

Stateful mocking with WireMock standalone.

## What This Skill Does
- Registers stubs at runtime through the Admin API
- Matches requests on method, URL, headers, and bodies
- Records live traffic and replays it as stubs
- Models stateful flows with scenarios

## When to Use
- Consumer-driven contract testing against a local stub
- Simulating flaky or failure modes of third-party APIs
- Recording a session of a legacy API for offline tests

## Real Commands

```bash
java -jar wiremock-standalone-3.9.1.jar --port 8080
curl -s -X POST http://localhost:8080/__admin/mappings -H 'Content-Type: application/json' \
  -d '{"request":{"method":"GET","url":"/hello"},"response":{"status":200,"body":"Hello"}}'
curl -s http://localhost:8080/hello
```

## Scenario Example

```json
{
  "scenarioName": "order",
  "requiredScenarioState": "Started",
  "request": { "method": "POST", "url": "/orders" },
  "response": { "status": 201, "jsonBody": { "id": "ord_1" } },
  "newScenarioState": "Created"
}
```

## Testing
- Assert stub hits with /__admin/requests
- Clear state between tests to avoid cross-test pollution
- Use proximity priorities for overlapping matchers

## Best Practices
- Store mappings as JSON files under mappings/ for reproducibility
- Use urlPathPattern with regex for path-parameterized endpoints
- Reset state in test teardown via the Admin API

## Capabilities

### wiremock-standalone
Run WireMock and register stub mappings dynamically

**Parameters:**
- `port` (integer): WireMock listen port
- `stub-json` (object): request matcher + response definition JSON
- `admin-root` (string): Base path of the Admin API (default /__admin)

**Commands:**
- `java -jar wiremock-standalone-3.9.1.jar --port 8080`
- `curl -s -X POST http://localhost:8080/__admin/mappings -H 'Content-Type: application/json' -d '{"request":{"method":"GET","url":"/hello"},"response":{"status":200,"body":"Hello"}}'`
- `curl -s http://localhost:8080/hello`
- `curl -s http://localhost:8080/__admin/mappings | jq '.mappings | length'`
- `curl -s -X DELETE http://localhost:8080/__admin/mappings`

**Examples:**
- POST to /__admin/mappings registers a new stub at runtime
- curl localhost:8080/hello resolves against registered stubs
- GET /__admin/mappings lists all active stubs

### record-playback
Record real traffic and replay it as stubs

**Commands:**
- `curl -s -X POST http://localhost:8080/__admin/recordings/start -d '{"targetBaseUrl":"http://localhost:8080"}' -H 'Content-Type: application/json'`
- `curl -s -X POST http://localhost:8080/__admin/recordings/stop -H 'Content-Type: application/json'`
- `curl -s http://localhost:8080/__admin/requests | jq '.requests | length'`
- `curl -s -X DELETE http://localhost:8080/__admin/requests -o /dev/null -w '%{http_code}\n'`

**Examples:**
- -cli --help
- -api --help

## References
- [WireMock Standalone](https://wiremock.org/docs/standalone/java-jar/)
- [WireMock Stubbing](https://wiremock.org/docs/stubbing/)