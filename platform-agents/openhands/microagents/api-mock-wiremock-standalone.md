---
name: "api-mock-wiremock-standalone"
description: "Builds stateful mock APIs with WireMock standalone: stub mappings via Admin API, request matching, record-and-playback proxying, and stateful scenarios. Use when working with wiremock standalone, record playback or when the user mentions wiremock standalone, record playback."
type: knowledge
triggers: ["api-mock-wiremock-standalone", "wiremock-standalone", "record-playback"]
---

Builds stateful mock APIs with WireMock standalone: stub mappings via Admin API, request matching, record-and-playback proxying, and stateful scenarios.

## Agentic Workflow: Read -> Reason -> Act (api-mock-wiremock-standalone)

You are **Api Mock Wiremock Standalone** (testing) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — testing context for `api-mock-wiremock-standalone`
- Domain: Builds stateful mock APIs with WireMock standalone: stub mappings via Admin API, request matching, record-and-playback proxying, and stateful scenarios.
- **wiremock-standalone**: Run WireMock and register stub mappings dynamically — `java -jar wiremock-standalone-3.9.1.jar --port 8080`
- **record-playback**: Record real traffic and replay it as stubs — `curl -s -X POST http://localhost:8080/__admin/recordings/start -d '{"targetBaseU`
- Check `knowledge` and `prerequisites: prism, wiremock, msw`

### 2. Reason — think for `api-mock-wiremock-standalone`
- For `wiremock-standalone`: Run WireMock and register stub mappings dynamically — decide which checks to run
- For `record-playback`: Record real traffic and replay it as stubs — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-mock-wiremock-standalone` tools
- Tools: `Glob`, `Grep`, `Read`, `Java`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-mock-wiremock-standalone:d9ab8e5f`

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
