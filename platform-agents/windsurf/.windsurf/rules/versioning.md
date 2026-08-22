---
trigger: glob
description: "Applies and verifies the four standard API versioning schemes: URI path, custom header, media type negotiation, and query parameter. Implements deprecation signaling with Deprecation and Sunset headers enabling smooth migrations."
globs: ["**/*.go", "**/*.json", "**/*.r", "**/*.sh"]
---

# Versioning

Applies and verifies the four standard API versioning schemes: URI path, custom header, media type negotiation, and query parameter. Implements deprecation signaling with Deprecation and Sunset headers enabling smooth migrations.

## Instructions

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
