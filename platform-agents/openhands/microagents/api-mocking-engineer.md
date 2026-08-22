---
name: "api-mocking-engineer"
description: "Evaluates and operates advanced mock server tools: Mountebank imposter protocol, Hoverfly simulation, and service virtualization for microservice test environments."
type: knowledge
triggers: ["api-mocking-engineer", "mountebank", "hoverfly"]
---

# api-mocking-engineer

Evaluates and operates advanced mock server tools: Mountebank imposter protocol, Hoverfly simulation, and service virtualization for microservice test environments.

## Instructions

# API Mocking Engineer

Service virtualization with Mountebank and Hoverfly.

## What This Skill Does
- Creates protocol-level mocks (HTTP, TCP, SMTP) with Mountebank
- Captures and replays traffic with Hoverfly
- Supports stateful and conditional mock responses

## When to Use
- Virtualizing downstream services for integration testing
- Simulating email/SMS providers over SMTP
- Replaying recorded traffic in CI environments

## Real Commands

```bash
mb start --port 2525
curl -s -X POST http://localhost:2525/imposters -H 'Content-Type: application/json' \
  -d '{"port":4545,"protocol":"http","stubs":[{"responses":[{"is":{"statusCode":200,"body":"ok"}}]}]}'
curl -s http://localhost:4545/anything
```

## Mountebank Predicates
- Deep equality: { deepEqual: { path: '/a' } }
- Contains: { contains: { body: 'error' } }
- JSONPath: { jsonpath: { selector: '$..status' } }
- Proxy: forward unmatched requests to a real target

## Testing
- Verify imposter state via the admin API
- Record traffic with Hoverfly, export simulations, replay offline

## Best Practices
- Use JSONPath predicates over brittle body matching
- Export simulations to files for CI reproducibility
- Prefer imposter scopes that mirror production topology

## Capabilities

### mountebank
Create protocol-level mock services (imposters) with Mountebank

**Commands:**
- `npm install -g mountebank`
- `mb start --port 2525`
- `curl -s -X POST http://localhost:2525/imposters -H 'Content-Type: application/json' -d '{"port":4545,"protocol":"http","stubs":[{"responses":[{"is":{"statusCode":200,"body":"ok"}}]}]}'`
- `curl -s http://localhost:4545/anything`
- `curl -s http://localhost:2525/imposters | jq '.imposters | length'`

**Examples:**
- mb start --port 2525 runs the Mountebank control plane
- POST /imposters with protocol http creates a mock on port 4545
- GET /imposters lists active mock services

### hoverfly
Simulate and record APIs with Hoverfly in capture mode

**Commands:**
- `docker run --name hoverfly -p 8888:8888 -p 8500:8500 spectolabs/hoverfly:latest`
- `curl -s -X PUT http://localhost:8888/api/v2/hoverfly/mode -d '{"mode":"capture"}' -H 'Content-Type: application/json'`
- `curl -s http://localhost:8500/api/v2/hoverfly/state`
- `curl -s -X PUT http://localhost:8888/api/v2/hoverfly/mode -d '{"mode":"simulate"}' -H 'Content-Type: application/json'`
