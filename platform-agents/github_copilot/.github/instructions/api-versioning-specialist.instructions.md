---
applyTo: "**/*.go **/*.json **/*.r **/*.sh"
---

Specializes in media-type and header API versioning: vendor MIME types, Accept header negotiation, Vary handling, and version metadata in responses.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -s -H 'Accept: application/vnd.myapi.v1+json' http://lo`, `curl -s -H 'X-API-Version: 2024-06-01' http://localhost:8080`
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

# API Versioning Specialist

Media-type and header versioning.

## What This Skill Does
- Negotiates versions through Accept headers
- Uses vendor MIME types and date headers
- Handles caching with Vary

## When to Use
- Public APIs requiring fine-grained versioning
- APIs where URLs must stay stable
- Caching layers with content negotiation

## Real Commands

```bash
curl -s -H 'Accept: application/vnd.myapi.v1+json' https://api.example.com/orders | jq '.meta.version'
curl -s -H 'X-API-Version: 2024-06-01' https://api.example.com/orders | jq '.meta.version'
curl -s -D- -H 'Accept: application/vnd.myapi.v2+json' https://api.example.com/orders | grep -i '^vary:'
```

## Header Strategy
- Vendor media type: application/vnd.api.v2+json
- Date-based: X-API-Version: 2024-06-01
- Query: ?api-version=2 (fallback)

## Testing
- Test each negotiation path
- Verify Vary headers on cached responses
- Confirm 406 for unknown versions


## Best Practices
- Set Vary: Accept to protect caches
- Prefer explicit version over defaults
- Document version selection for clients

## Capabilities

### media-type-versioning
Negotiate versions via media types

**Parameters:**
- `media-type` (string): application/vnd.myapi.vN+json
- `version` (integer): Version number
- `format` (string): json, xml suffix

**Commands:**
- `curl -s -H 'Accept: application/vnd.myapi.v1+json' http://localhost:8080/orders | jq '.meta.version'`
- `curl -s -H 'Accept: application/vnd.myapi.v2+json' http://localhost:8080/orders | jq '.meta.version'`
- `curl -s -D- -H 'Accept: application/vnd.myapi.v2+json' http://localhost:8080/orders | grep -i '^vary:'`
- `curl -s -H 'Accept: application/json' http://localhost:8080/orders -o /dev/null -w '%{http_code}\n'`

**Examples:**
- Vendor media types carry the version
- Vary: Accept keeps caches honest
- Unversioned Accept can default or 406

### header-versioning
Use custom headers for version selection

**Commands:**
- `curl -s -H 'X-API-Version: 2024-06-01' http://localhost:8080/orders | jq '.meta.version'`
- `curl -s -H 'API-Version: 2' http://localhost:8080/orders | jq '.apiVersion'`
- `curl -s -o /dev/null -w '%{http_code}\n' -H 'X-API-Version: 1990-01-01' http://localhost:8080/orders`

**Examples:**
- -cli --help
- -api --help

## References
- [RFC 6838 - Media Types](https://www.rfc-editor.org/rfc/rfc6838)
- [Stripe Versioning](https://docs.stripe.com/api/versioning)
