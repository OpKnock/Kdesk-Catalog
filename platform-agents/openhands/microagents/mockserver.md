---
name: "mockserver"
description: "Mocks HTTP and HTTPS APIs with MockServer, creating expectations via REST admin API and proxying to real backends."
type: knowledge
triggers: ["mockserver", "mockserver-start", "expectation-management", "request-verification"]
---

# mockserver

Mocks HTTP and HTTPS APIs with MockServer, creating expectations via REST admin API and proxying to real backends.

## Instructions

# MockServer

Mock HTTP/HTTPS APIs for development and testing.

## What This Skill Does

- Starts MockServer locally or via Docker
- Creates expectations for paths, methods, and bodies
- Proxies unmatched requests to real backends
- Verifies which requests were received

## When to Use

- Frontend development without a backend
- Testing failure and edge-case responses
- Contract-ish testing against stubbed APIs

## Real Commands

```bash
# Start
java -jar mockserver-netty-jar-with-dependencies.jar -serverPort 1080
docker run -d -p 1080:1080 --name mockserver mockserver/mockserver

# Create expectation
curl -s -X PUT http://localhost:1080/mockserver/expectation -d '{
  "httpRequest": {"path": "/api/users", "method": "GET"},
  "httpResponse": {"statusCode": 200, "body": "{\"users\":[]}"}
}'

# Proxy everything else
curl -s -X PUT http://localhost:1080/mockserver/expectation -d '{
  "httpRequest": {"path": "/api/*"},
  "httpForward": {"host": "real-api", "port": 8080}
}'

# Verify calls
curl -s http://localhost:1080/mockserver/requests -d '{"path":"/api/users"}'

# Reset
curl -s -X PUT http://localhost:1080/mockserver/reset
```

## Best Practices

- Load initial expectations from JSON for reproducible setups
- Use proxying to mix mocked and real endpoints
- Reset state between test suites
- Verify request counts for call-order assertions
- Keep mock bodies consistent with the real contract

## Capabilities

### mockserver-start
Start MockServer locally or in Docker.

**Commands:**
- `java -jar mockserver-netty-jar-with-dependencies.jar -serverPort 1080`
- `docker run -d -p 1080:1080 --name mockserver mockserver/mockserver`
- `node mockserver-cli.js -serverPort 1080`
- `docker run -d -p 1080:1080 -e MOCKSERVER_INITIALIZATION_JSON_PATH=/config/init.json -v ./init.json:/config/init.json mockserver/mockserver`

**Examples:**
- docker run -d -p 1080:1080 --name mockserver mockserver/mockserver
- java -jar mockserver-netty-jar-with-dependencies.jar -serverPort 1080
- docker run -d -p 1080:1080 -e MOCKSERVER_INITIALIZATION_JSON_PATH=/config/init.json -v ./init.json:/config/init.json mockserver/mockserver

### expectation-management
Create, inspect, and clear expectations via the admin API.

**Commands:**
- `curl -s -X PUT http://localhost:1080/mockserver/expectation -d '{"httpRequest":{"path":"/api/users","method":"GET"},"httpResponse":{"statusCode":200,"body":"{\"users\":[]}"}}'`
- `curl -s -X PUT http://localhost:1080/mockserver/expectation -d '{"httpRequest":{"path":"/api/users/1"},"httpResponse":{"statusCode":404}}'`
- `curl -s http://localhost:1080/mockserver/expectation`
- `curl -s -X PUT http://localhost:1080/mockserver/reset`
- `curl -s -X PUT http://localhost:1080/mockserver/clear -d '{"path":"/api/orders"}'`

**Examples:**
- curl -s -X PUT http://localhost:1080/mockserver/expectation -d '{"httpRequest":{"path":"/api/users","method":"GET"},"httpResponse":{"statusCode":200,"body":"{\"users\":[]}"}}'
- curl -s http://localhost:1080/mockserver/expectation
- curl -s -X PUT http://localhost:1080/mockserver/reset

### request-verification
Inspect received requests and proxy behavior.

**Commands:**
- `curl -s http://localhost:1080/mockserver/requests -d '{"path":"/api/users"}'`
- `curl -s -X PUT http://localhost:1080/mockserver/expectation -d '{"httpRequest":{"path":"/api/*"},"httpForward":{"host":"real-api","port":8080}}'`
- `curl -s -X PUT http://localhost:1080/mockserver/verify -d '{"path":"/api/users","method":"POST","times":{"atLeast":1}}'`

**Examples:**
- curl -s http://localhost:1080/mockserver/requests -d '{"path":"/api/users"}'
- curl -s -X PUT http://localhost:1080/mockserver/verify -d '{"path":"/api/users","method":"POST"}'
