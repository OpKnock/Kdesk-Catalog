---
applyTo: "**/*.json **/*.r **/*.sh"
---

Implement correlation/request IDs across APIs: generate, propagate via headers, and trace requests through logs.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -H "X-Correlation-ID: $(uuidgen)" https://httpbin.org/g`, `npm install express`
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

# Correlation IDs

Trace a single request across services and logs with correlation IDs.

## When to Use

- Debugging multi-service requests
- Joining logs and metrics across services
- Supporting user support tickets with trace IDs

## Naming Conventions

Use X-Correlation-ID for cross-service traces and X-Request-ID for the immediate request; return it in the response.

## Generate and Send

```bash
uuidgen
curl -H "X-Correlation-ID: $(uuidgen)" https://httpbin.org/get
```

## Middleware (Express)

```js
const crypto = require('crypto');

app.use((req, res, next) => {
  const cid = req.headers['x-correlation-id'] || crypto.randomUUID();
  req.correlationId = cid;
  res.setHeader('X-Correlation-ID', cid);
  next();
});
```

## Propagate Downstream

```js
const headers = { 'X-Correlation-ID': req.correlationId };
fetch(downstreamUrl, { headers });
```

## Log With the ID

```js
console.log(JSON.stringify({ correlationId: cid, level: 'info', message: 'checkout started' }));
```

## Verify

```bash
node server.js &
curl -s -D - -o /dev/null http://localhost:8080/api | grep -i correlation
CID=$(uuidgen)
curl -s -D - -o /dev/null -H "X-Correlation-ID: $CID" http://localhost:8080/api | grep -i correlation
```

## Testing

```bash
# Same ID must be echoed back in the response
curl -s -D - -o /dev/null -H "X-Correlation-ID: test-123" http://localhost:8080/api | grep -i 'correlation'
```

## Best Practices

- Accept and echo inbound IDs, never regenerate them
- Propagate to every downstream call
- Include the ID in every log line and error response
- Cap ID length and sanitize header values
- Add a correlation ID to distributed traces (OpenTelemetry trace_id)
- Standardize the header name across the org

## Capabilities

### id-generation
Generate and send correlation IDs with curl and system tools

**Parameters:**
- `header` (string): Header name such as X-Correlation-ID
- `id` (string): Correlation ID value

**Commands:**
- `curl -H "X-Correlation-ID: $(uuidgen)" https://httpbin.org/get`
- `uuidgen`
- `curl -H "X-Request-ID: $(uuidgen)" -H "X-Correlation-ID: $(uuidgen)" https://httpbin.org/uuid`
- `curl -s -D - -o /dev/null https://httpbin.org/get | grep -i correlation`

**Examples:**
- curl -H "X-Correlation-ID: $(uuidgen)" https://httpbin.org/get | jq '.trace_id'
- CID=$(uuidgen) && curl -H "X-Correlation-ID: $CID" https://httpbin.org/uuid
- curl -s -D - -o /dev/null -H "X-Correlation-ID: $(uuidgen)" https://httpbin.org/get | grep -i 'correlation\|request-id'

### middleware
Implement correlation ID middleware that accepts, generates, and propagates IDs

**Parameters:**
- `server_port` (string): Server port for testing

**Commands:**
- `npm install express`
- `node server.js`
- `curl -s -D - -o /dev/null -H "X-Correlation-ID: $(uuidgen)" http://localhost:8080/api | grep -i correlation`
- `curl -s http://localhost:8080/api -D - -o /dev/null | grep -i correlation`

**Examples:**
- node server.js
- curl -s -D - -o /dev/null -H "X-Correlation-ID: test-123" http://localhost:8080/api | grep -i correlation
- curl -s -D - -o /dev/null http://localhost:8080/api | grep -i correlation

## References
- [Zalando REST API Guidelines](https://opensource.zalando.com/restful-api-guidelines/)
- [Microsoft Correlation Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/correlation-id)
