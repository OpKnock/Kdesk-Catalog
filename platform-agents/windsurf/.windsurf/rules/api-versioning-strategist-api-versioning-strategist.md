---
trigger: glob
description: "Selects API versioning strategies: comparing URL, header, media-type, and query approaches against consumer constraints, and documenting decisions. Use when working with strategy comparison, decision docs or when the user mentions strategy comparison, decision docs."
globs: ["**/*.go", "**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

Selects API versioning strategies: comparing URL, header, media-type, and query approaches against consumer constraints, and documenting decisions.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -s -H 'Accept: application/vnd.github.v3+json' https://`, `curl -s http://localhost:8080/docs/versioning | jq '.strateg`
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
