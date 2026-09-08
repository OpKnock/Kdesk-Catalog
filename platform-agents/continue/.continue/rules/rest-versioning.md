---
name: "Rest Versioning"
description: "Expert reference covering Accept-header and URL versioning, cursor pagination, conditional requests, and Prefer response selection. Use when working with rest versioning, api or when the user mentions rest versioning, api."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
alwaysApply: false
---

Expert reference covering Accept-header and URL versioning, cursor pagination, conditional requests, and Prefer response selection.

## Agentic Workflow: Read -> Reason -> Act (rest-versioning)

You are **Rest Versioning** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `rest-versioning`
- Domain: Expert reference covering Accept-header and URL versioning, cursor pagination, conditional requests, and Prefer response selection.
- **rest-versioning**: Versioned REST design: media types, cursors, conditional requests — `curl -s -H 'Accept: application/vnd.myapi.v2+json' https://api.your-app.test/use`
- Check `knowledge` references before acting

### 2. Reason — think for `rest-versioning`
- For `rest-versioning`: Versioned REST design: media types, cursors, conditional requests — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `rest-versioning` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `rest-versioning:ba13df60`

# REST API Versioning (v2 conventions)

Expert skill for versioned REST APIs with cursor pagination and conditional requests.

## What this skill does

- Version APIs via Accept media types instead of URL breaking changes
- Paginates with opaque cursors instead of page numbers
- Uses ETags, If-None-Match, and Prefer headers to save bandwidth

## When to use

- Launching a breaking change to an existing API
- Adding fields that existing clients must not see
- Optimizing list endpoints used by mobile clients

## Real commands

```bash
# Pick the version with the Accept header
curl -s -H 'Accept: application/vnd.myapi.v2+json' https://api.your-app.test/users

# Cursor pagination: read the next cursor from the response
curl -s 'https://api.your-app.test/users?cursor=abc123&limit=100' | jq '.next_cursor'

# Conditional GET: 304 if nothing changed
curl -i https://api.your-app.test/users/42
curl -s -H 'If-None-Match: "etag-42"' -o /dev/null -w '%{http_code}\n' https://api.your-app.test/users/42

# Ask the server to return the updated representation
curl -s -H 'Prefer: return=representation' -X PATCH https://api.your-app.test/users/42 -d '{"name":"Ada"}'
```

## Design rules

- Never change response shape of a live version; add a new version
- Cursors are opaque: clients must not decode or construct them
- List endpoints return {items, next_cursor} and drop cursor support at the end

## Testing

```bash
# Paginate until next_cursor is null
curl -s 'https://api.your-app.test/users?limit=100'
curl -s 'https://api.your-app.test/users?cursor=abc123&limit=100'
```

## Best practices

- Keep at least one version overlapping during migrations
- Deprecate old versions with a Sunset header and changelog
- Validate ETags on writes with If-Match to prevent lost updates

## Capabilities

### rest-versioning
Versioned REST design: media types, cursors, conditional requests

**Parameters:**
- `accept_header` (string): Media type selecting the API version, e.g. application/vnd.myapi.v2+json
- `cursor` (string): Opaque pagination token from the previous page
- `limit` (integer): Page size for list endpoints

**Commands:**
- `curl -s -H 'Accept: application/vnd.myapi.v2+json' https://api.your-app.test/users`
- `curl -s 'https://api.your-app.test/users?cursor=abc123&limit=100' | jq '.next_cursor'`
- `curl -i https://api.your-app.test/users/42`
- `curl -s -H 'If-None-Match: "etag-42"' https://api.your-app.test/users/42`
- `curl -s -H 'Prefer: return=representation' -X PATCH https://api.your-app.test/users/42 -d '{"name":"Ada"}'`

**Examples:**
- curl -s 'https://api.your-app.test/users?cursor=abc123&limit=100'
- curl -i -H 'Accept: application/vnd.myapi.v2+json' https://api.your-app.test/users
- curl -s -H 'If-None-Match: "etag-42"' -o /dev/null -w '%{http_code}\n' https://api.your-app.test/users/42

## References
- [Microsoft REST API Guidelines](https://github.com/microsoft/api-guidelines/blob/vNext/Guidelines.md)
- [RFC 9110 Prefer header](https://www.rfc-editor.org/rfc/rfc9110#section-12.5.4)