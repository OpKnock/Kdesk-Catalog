---
type: agent_requested
description: "Applies and verifies the four standard API versioning schemes: URI path, custom header, media type negotiation, and query parameter. Implements deprecation signaling with Deprecation and Sunset headers enabling smooth migrations. Use when working with versioning schemes, api, rest or when the user mentions versioning schemes, api, rest."
---

Applies and verifies the four standard API versioning schemes: URI path, custom header, media type negotiation, and query parameter. Implements deprecation signaling with Deprecation and Sunset headers enabling smooth migrations.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -s https://api.your-app.test/v2/users`
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

# API Versioning

## What this skill does

Design versioning for APIs. Covers the four main schemes - URI path, query string, custom header, and
media type negotiation - plus deprecation signaling with Deprecation and Sunset headers.

## When to use

- Adding breaking changes to an existing API
- Migrating consumers to a new endpoint shape
- Choosing a scheme for a greenfield API

## Real commands

```bash
# URI path versioning
curl -s https://api.your-app.test/v2/users

# Custom header versioning
curl -s -H "X-Api-Version: 2024-01-15" https://api.your-app.test/users

# Media type (content negotiation) versioning
curl -s -H "Accept: application/vnd.example.v2+json" https://api.your-app.test/users
curl -s -H "Accept: application/vnd.example+json;version=2" https://api.your-app.test/users

# Query string versioning
curl -s "https://api.your-app.test/users?api-version=2"

# Verify deprecation signaling
curl -sI https://api.your-app.test/v1/users | grep -iE "deprecation|sunset"

# Compare versions side by side
diff <(curl -s https://api.your-app.test/v1/users | jq -S .) <(curl -s https://api.your-app.test/v2/users | jq -S .)
```

## Header conventions

```http
Deprecation: true
Sunset: Fri, 31 Jan 2025 23:59:59 GMT
```

## Best practices

- Never remove a version without a published Sunset date
- Keep at least 6 months between deprecation and sunset
- Route versions at the gateway, not inside controllers
- Document the versioning policy in the API reference

## Testing

```bash
curl -s https://api.your-app.test/v1/users -o /dev/null -w "%{http_code}\n"
curl -s -H "X-Api-Version: 9999-01-01" https://api.your-app.test/users -o /dev/null -w "%{http_code}\n"
```

## Capabilities

### versioning-schemes
Apply and verify the four standard API versioning schemes

**Parameters:**
- `version` (string): Version value used in path, query, or header
- `media_type` (string): Custom media type for content negotiation versioning

**Commands:**
- `curl -s https://api.your-app.test/v2/users`
- `curl -s -H "X-Api-Version: 2024-01-15" https://api.your-app.test/users`
- `curl -s -H "Accept: application/vnd.example.v2+json" https://api.your-app.test/users`
- `curl -s "https://api.your-app.test/users?api-version=2"`
- `curl -sI https://api.your-app.test/v1/users | grep -iE "deprecation|sunset"`

**Examples:**
- curl -s -H "Accept: application/vnd.example+json;version=2" https://api.your-app.test/users | jq ".schema"
- curl -sI https://api.your-app.test/v2/users | grep -i sunset
- curl -s "https://api.your-app.test/users?api-version=1" -o /dev/null -w "%{http_code}"

## References
- [Azure API Design Best Practices](https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design)
- [RFC 8594 - Sunset Header](https://datatracker.ietf.org/doc/html/rfc8594)
- [Stripe API Versioning](https://stripe.com/docs/api/versioning)