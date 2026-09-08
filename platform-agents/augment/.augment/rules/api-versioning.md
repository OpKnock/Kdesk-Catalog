---
type: agent_requested
description: "Implements general API versioning across backend services: strategy selection, version headers, backward compatibility, and version-aware routing. Use when working with version headers, compatibility, backend or when the user mentions version headers, compatibility, backend."
---

Implements general API versioning across backend services: strategy selection, version headers, backward compatibility, and version-aware routing.

## Agentic Workflow: Read -> Reason -> Act (api-versioning)

You are **Api Versioning** (backend/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `api-versioning`
- Domain: Implements general API versioning across backend services: strategy selection, version headers, backward compatibility, and version-aware routing.
- **version-headers**: Serve versions via headers and negotiation — `curl -s -H 'Accept: application/vnd.github.v3+json' https://api.github.com/repos`
- **compatibility**: Maintain backward compatibility — `curl -s -o /dev/null -w '%{http_code}\n' http://localhost:3000/v1/users`
- Check `knowledge` and `prerequisites: git`

### 2. Reason — think for `api-versioning`
- For `version-headers`: Serve versions via headers and negotiation — decide which checks to run
- For `compatibility`: Maintain backward compatibility — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-versioning` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-versioning:ddc67614`

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

**Parameters:**
- `header` (string): Version header name
- `version` (string): Version value
- `media-type` (string): Vendor media type

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

**Examples:**
- general-cli --help
- general-api --help

## References
- [Microsoft API Versioning Guidance](https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design#versioning)
- [GitHub REST Versions](https://docs.github.com/en/rest/about-the-rest-api/api-versions)