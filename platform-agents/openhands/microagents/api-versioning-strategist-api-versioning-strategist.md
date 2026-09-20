---
name: "api-versioning-strategist-api-versioning-strategist"
description: "Selects API versioning strategies: comparing URL, header, media-type, and query approaches against consumer constraints, and documenting decisions."
type: knowledge
triggers: ["api-versioning-strategist-api-versioning-strategist", "strategy-comparison", "decision-docs"]
---

# api-versioning-strategist-api-versioning-strategist

Selects API versioning strategies: comparing URL, header, media-type, and query approaches against consumer constraints, and documenting decisions.

## Instructions

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
