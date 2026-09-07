Implements general API versioning across backend services: strategy selection, version headers, backward compatibility, and version-aware routing.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -s -H 'Accept: application/vnd.github.v3+json' https://`, `curl -s -o /dev/null -w '%{http_code}\n' http://localhost:30`
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