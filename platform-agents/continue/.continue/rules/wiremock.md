---
name: "wiremock"
description: "Stubs HTTP APIs with WireMock standalone, managing mappings, requests journal, and delays via the admin API."
globs: ["**/*.java", "**/*.json", "**/*.r", "**/*.sh"]
alwaysApply: false
---

# wiremock

Stubs HTTP APIs with WireMock standalone, managing mappings, requests journal, and delays via the admin API.

## Instructions

# WireMock

API stubbing for tests and development.

## What This Skill Does

- Serves stubbed responses for any HTTP API
- Creates mappings via the admin REST API
- Simulates delays, faults, and failures
- Journals requests for verification


## When to Use

- Frontend dev against a stubbed backend
- Testing error and latency scenarios
- Contract verification in integration tests

## Real Commands

```bash
# Start
java -jar wiremock-standalone.jar --port 8080
docker run -d -p 8080:8080 --name wiremock wiremock/wiremock

# Stub a mapping
curl -X POST http://localhost:8080/__admin/mappings -d '{
  "request": {"method": "GET", "url": "/api/users"},
  "response": {"status": 200, "jsonBody": {"users": []}}
}'

# Simulate delay
curl -X POST http://localhost:8080/__admin/mappings -d '{
  "request": {"method": "GET", "url": "/api/users"},
  "response": {"fixedDelayMilliseconds": 2000, "status": 200}
}'

# Verify requests
curl -s http://localhost:8080/__admin/requests
curl -X POST http://localhost:8080/__admin/requests/reset
```

## Best Practices

- Load mappings from __files + mappings dir at startup
- Reset state between test suites
- Use response templating for dynamic data
- Verify request counts for call assertions
- Mirror the real API contract in stubs

## Capabilities

### wiremock-start
Start WireMock standalone or in Docker.

**Commands:**
- `java -jar wiremock-standalone.jar --port 8080`
- `docker run -d -p 8080:8080 --name wiremock wiremock/wiremock`
- `java -jar wiremock-standalone.jar --root-dir stubs --port 8080 --verbose`
- `docker run -d -p 8080:8080 -v $PWD/stubs:/home/wiremock wiremock/wiremock`

**Examples:**
- docker run -d -p 8080:8080 --name wiremock wiremock/wiremock
- java -jar wiremock-standalone.jar --root-dir stubs --port 8080
- docker run -d -p 8080:8080 -v $PWD/stubs:/home/wiremock wiremock/wiremock

### stub-mappings
Create and manage stub mappings via admin API.

**Commands:**
- `curl -X POST http://localhost:8080/__admin/mappings -d '{"request":{"method":"GET","url":"/api/users"},"response":{"status":200,"jsonBody":{"users":[]}}}'`
- `curl -s http://localhost:8080/__admin/mappings`
- `curl -X DELETE http://localhost:8080/__admin/mappings/{id}`
- `curl -X POST http://localhost:8080/__admin/mappings/reset`
- `curl -s -X POST http://localhost:8080/__admin/mappings -d '{"request":{"method":"GET","url":"/api/users"},"response":{"fixedDelayMilliseconds":2000,"status":200}}'`

**Examples:**
- curl -X POST http://localhost:8080/__admin/mappings -d '{"request":{"method":"GET","url":"/api/users"},"response":{"status":200,"jsonBody":{"users":[]}}}'
- curl -s http://localhost:8080/__admin/mappings
- curl -X POST http://localhost:8080/__admin/mappings/reset

### requests-journal
Verify received requests.

**Commands:**
- `curl -s http://localhost:8080/__admin/requests`
- `curl -s http://localhost:8080/__admin/requests?limit=10`
- `curl -X POST http://localhost:8080/__admin/requests/reset`
- `curl -s http://localhost:8080/__admin/requests/find -d '{"method":"POST","url":"/api/orders"}'`

**Examples:**
- curl -s http://localhost:8080/__admin/requests
- curl -X POST http://localhost:8080/__admin/requests/reset
- curl -s http://localhost:8080/__admin/requests/find -d '{"method":"POST","url":"/api/orders"}'