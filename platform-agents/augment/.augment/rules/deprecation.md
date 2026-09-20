---
type: agent_requested
description: "Manages endpoint phase-out lifecycle: Sunset headers, spec linting for metadata, and usage auditing before removal."
---

# Deprecation

Manages endpoint phase-out lifecycle: Sunset headers, spec linting for metadata, and usage auditing before removal.

## Instructions

# API Phase-Out

## What this skill does

Endpoint phase-out management is the discipline of announcing, phasing, and removing API features without breaking consumers. This skill covers the Sunset headers, spec linting for metadata, and migration auditing.

## When to use

- Planning the retirement of a v1 endpoint in favor of v2
- Enforcing that all retired operations carry metadata in the OpenAPI spec
- Auditing which consumers still call an endpoint before removal

## Real commands

```bash
# Lint the spec so every removed-in-future operation is marked
spectral lint openapi.yaml -r .spectral/deprecation.rules.yml

# Probe a live endpoint for sunset headers
curl -sI https://httpbin.org/headers -H 'Authorization: Bearer $TOKEN' | grep -iE '^(deprecation|sunset|link):'

# Count retired operations in the spec
npx @redocly/cli lint openapi.yaml --skip-rule operation-4xx-response

# Find who still uses the endpoint in server logs
zgrep -h 'GET /v1/legacy' /var/log/nginx/access.log*.gz | awk '{print $1}' | sort | uniq -c | sort -rn
```

## Header example

```http
HTTP/1.1 200 OK
Deprecation: true
Sunset: Sat, 31 Dec 2026 23:59:59 GMT
Link: <https://api.example.com/v2/users>; rel="successor-version"
```

## OpenAPI metadata example

```yaml
paths:
  /v1/legacy:
    get:
      deprecated: true
      description: Use GET /v2/users instead.
```

## Best practices

- Always ship a successor: a retired endpoint with no replacement is a trap.
- Give at least 6-12 months between announcement and the Sunset date.
- Include the `sunset` date in the header so clients can schedule migration automatically.
- Log warnings server-side and report usage metrics before removal.
- Remove the endpoint only when traffic falls below the agreed threshold.

## Testing

```bash
# Verify the header is present on every version of the endpoint
curl -sI https://httpbin.org/headers | grep -qi '^deprecation:'; echo $?
```

## Capabilities

### deprecation-audit
Lint OpenAPI specs for missing metadata and probe live endpoints for sunset headers.

**Commands:**
- `spectral lint openapi.yaml -r .spectral/deprecation.rules.yml`
- `curl -sI https://httpbin.org/headers -H 'Authorization: Bearer $TOKEN' | grep -iE '^(deprecation|sunset|link):'`
- `grep -n 'deprecated: true' openapi.yaml | wc -l`
- `npx @redocly/cli lint openapi.yaml --skip-rule operation-4xx-response`
- `curl -s https://httpbin.org/get | jq '.meta.deprecation'`

**Examples:**
- spectral lint openapi.yaml -r .spectral/deprecation.rules.yml
- curl -sI https://httpbin.org/headers -H 'Authorization: Bearer $TOKEN' | grep -i 'sunset:'
- grep -rn 'deprecated: true' specs/*.yaml