# Api Versioning

Implements general API versioning across backend services: strategy selection, version headers, backward compatibility, and version-aware routing.

## Instructions

# API Versioning

Versioning across backend services.

## What This Skill Does
- Selects and implements versioning strategies
- Keeps old versions compatible
- Routes versioned traffic correctly

## When to Use
- Multiple client generations
- Breaking changes with legacy consumers
- Version-aware gateway routing

## Real Commands

```bash
curl -s -H 'Accept: application/vnd.github.v3+json' https://api.github.com/repos/octocat/Hello-World | jq '.full_name'
curl -s -H 'X-API-Version: 2' http://localhost:3000/api/users | jq '.version'
```

## Strategy Selection
- URL: /v1, /v2 - visible and simple
- Header: clean URLs, explicit selection
- Media type: RESTful negotiation

## Testing
- Verify every version endpoint
- Test unknown versions fail cleanly
- Confirm caching honors Vary


## Best Practices
- Deprecate slowly with sunset dates
- Keep defaults stable
- Document versions in OpenAPI

## Capabilities

### version-headers
Serve versions via headers and negotiation

**Commands:**
- `curl -s -H 'Accept: application/vnd.github.v3+json' https://api.github.com/repos/octocat/Hello-World | jq '.full_name'`
- `curl -s -H 'X-API-Version: 2' http://localhost:3000/api/users | jq '.version'`
- `curl -s -H 'X-API-Version: 1' http://localhost:3000/api/users | jq '.version'`
- `curl -s -D- -H 'Accept: application/vnd.api.v2+json' http://localhost:3000/api/users | grep -i '^vary:'`

**Examples:**
- Accept headers negotiate media-type versions
- X-API-Version selects explicit versions
- Vary: Accept protects caches

### compatibility
Maintain backward compatibility

**Commands:**
- `curl -s -o /dev/null -w '%{http_code}\n' http://localhost:3000/v1/users`
- `curl -s http://localhost:3000/v2/users | jq '.fields | keys'`
- `curl -s -o /dev/null -w '%{http_code}\n' http://localhost:3000/v9/users`
- `git tag -l 'v*' --sort=-v:refname | head -3`
