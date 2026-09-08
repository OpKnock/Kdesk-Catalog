---
name: "api-versioning-strategist-api-versioning-strategist"
description: "Selects API versioning strategies: comparing URL, header, media-type, and query approaches against consumer constraints, and documenting decisions. Use when working with strategy comparison, decision docs or when the user mentions strategy comparison, decision docs."
license: "MIT"
compatibility: "Requires node.js, python, openapi-generator, postman, stoplight-studio. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "backend"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(npx:*)"
---

Selects API versioning strategies: comparing URL, header, media-type, and query approaches against consumer constraints, and documenting decisions.

## Agentic Workflow: Read -> Reason -> Act (api-versioning-strategist-api-versioning-strategist)

You are **api-versioning-strategist-api-versioning-strategist** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `api-versioning-strategist-api-versioning-strategist`
- Domain: Selects API versioning strategies: comparing URL, header, media-type, and query approaches against consumer constraints, and documenting decisions.
- **strategy-comparison**: Evaluate versioning strategies against requirements — `curl -s -H 'Accept: application/vnd.github.v3+json' https://api.github.com/repos`
- **decision-docs**: Document versioning decisions — `curl -s http://localhost:8080/docs/versioning | jq '.strategies'`
- Check `knowledge` and `prerequisites: node.js, python, openapi-generator`

### 2. Reason — think for `api-versioning-strategist-api-versioning-strategist`
- For `strategy-comparison`: Evaluate versioning strategies against requirements — decide which checks to run
- For `decision-docs`: Document versioning decisions — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-versioning-strategist-api-versioning-strategist` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-versioning-strategist-api-versioning-strategist:d93a6d04`

# API Versioning Strategist

Versioning strategy selection.

## What This Skill Does
- Compares versioning strategies objectively
- Matches strategies to consumer constraints
- Documents decisions and tradeoffs

## When to Use
- Choosing a versioning approach
- Reviewing existing versioning pain
- Aligning teams on one strategy

## Real Commands

```bash
curl -s -H 'Accept: application/vnd.github.v3+json' https://api.github.com/repos/octocat/Hello-World | jq '.full_name'
npx @redocly/cli lint openapi.yaml
```

## Strategy Matrix
- URL: simple, visible, common (v1, v2)
- Header: clean URLs, cache complexity
- Media type: RESTful, negotiation-based
- Query: simplest, least explicit

## Testing
- Prototype the top two strategies
- Measure client migration effort
- Validate docs generation for each


## Best Practices
- Default to URL versioning for public APIs
- Use media types when content varies by version
- Document the strategy in the OpenAPI spec

## Capabilities

### strategy-comparison
Evaluate versioning strategies against requirements

**Parameters:**
- `strategy` (string): url, header, media-type, query, or hybrid
- `consumer` (string): Consumer type: browser, SDK, third-party
- `spec` (string): OpenAPI doc path

**Commands:**
- `curl -s -H 'Accept: application/vnd.github.v3+json' https://api.github.com/repos/octocat/Hello-World | jq '.full_name'`
- `curl -s https://api.github.com/repos/octocat/Hello-World | jq '.full_name'`
- `npx @redocly/cli lint openapi.yaml`
- `curl -sI http://localhost:8080/v2/health | head -1`

**Examples:**
- GitHub uses Accept-header versioning
- URL versioning is simplest to observe
- Redocly lint validates the documented strategy

### decision-docs
Document versioning decisions

**Commands:**
- `curl -s http://localhost:8080/docs/versioning | jq '.strategies'`
- `npx swagger-cli validate openapi.yaml`
- `curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8080/v2/health`

**Examples:**
- -cli --help
- -api --help

## References
- [GitHub REST Versioning](https://docs.github.com/en/rest/about-the-rest-api/api-versions)
- [Google API Design Guide](https://google.aip.dev/general/0135)
