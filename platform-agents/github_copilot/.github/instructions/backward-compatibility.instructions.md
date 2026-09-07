---
applyTo: "**/*.json **/*.r **/*.sh **/*.{yaml,yml}"
---

Enforces API evolution safety with semantic versioning discipline, additive-only schema changes, media-type and URL-path versioning, and automated breaking-change detection between OpenAPI specifications.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm version minor`, `curl -s -H "Accept: application/vnd.myapi.v2+json" https://a`
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

# Backward Compatibility

## What this skill does

Enforces API evolution safety with semantic versioning discipline, additive-only schema changes, media-type and URL-path versioning, and automated breaking-change detection between OpenAPI specifications.

## When to use

- Planning a release that touches public API contracts
- Evaluating whether a spec change is breaking
- Setting up CI gates against spec drift

## Real commands

```bash
# Version bumps
npm version minor
npm version patch -m "release %s"
git tag v2.0.0

# Test versioned endpoints
curl -s -H "Accept: application/vnd.myapi.v2+json" https://api.your-app.test/users
curl -s https://api.your-app.test/v1/users

# Breaking change detection
npx openapi-diff old.yaml new.yaml | grep -i breaking
npx @redocly/cli lint new.yaml
```

## Rules of thumb

- Adding an optional field/parameter: compatible
- Removing or renaming a field: breaking (major)
- Changing a required field to optional: usually safe; reverse is not

## Testing

- Run openapi-diff in CI on every spec change
- Keep a compat test calling v1 endpoints after v2 ships

## Best practices

- Deprecate with headers and docs, then remove after a published timeline
- Use additive evolutions (openapi-diff 'non-breaking') as the default
- Pin clients to media-type versions to decouple releases

## Capabilities

### semver
Apply semantic versioning rules to releases.

**Parameters:**
- `version_bump` (string): major, minor, or patch
- `range` (string): Semver range expression

**Commands:**
- `npm version minor`
- `npm version major`
- `git tag v2.0.0`
- `npx semver --range "^1.0.0" 1.5.0`
- `git diff v1.0.0 v2.0.0 --stat`

**Examples:**
- npm version patch -m "release %s"
- git tag -a v1.1.0 -m "additive release"
- npx semver --coerce "v1.2.3"

### api-versioning
Version APIs via media types or URL prefixes.

**Parameters:**
- `accept_header` (string): Media type version header
- `base_url` (string): API base URL

**Commands:**
- `curl -s -H "Accept: application/vnd.myapi.v2+json" https://api.your-app.test/users`
- `curl -s -H "Accept: application/vnd.myapi.v1+json" https://api.your-app.test/users`
- `curl -s https://api.your-app.test/v2/users?limit=10`
- `curl -s https://api.your-app.test/v1/users`
- `curl -s -H "Api-Version: 2026-01-01" https://api.your-app.test/users`

**Examples:**
- curl -s -H "Accept: application/vnd.myapi.v2+json" https://api.your-app.test/users | jq '.schema'
- curl -s https://api.your-app.test/v1/users -o v1.json && curl -s https://api.your-app.test/v2/users -o v2.json && diff v1.json v2.json
- curl -s -o /dev/null -w "%{http_code}\n" -H "Accept: application/vnd.myapi.v99+json" https://api.your-app.test/users

### compat-checks
Detect breaking changes between specs.

**Parameters:**
- `old_spec` (string): Baseline OpenAPI spec
- `new_spec` (string): Candidate OpenAPI spec

**Commands:**
- `npx openapi-diff old.yaml new.yaml`
- `npx @redocly/cli lint new.yaml`
- `npx swagger-cli validate new.yaml`
- `npx openapi-changes compare old.yaml new.yaml`
- `git diff --exit-code v1.0.0 v1.1.0 -- openapi.yaml`

**Examples:**
- npx openapi-diff old.yaml new.yaml | grep -i breaking
- npx @redocly/cli lint --extends minimal new.yaml
- npx openapi-changes compare old.yaml new.yaml --json

## References
- [Semantic Versioning](https://semver.org/)
- [openapi-diff](https://github.com/OpenAPITools/openapi-diff)
- [Redocly CLI](https://redocly.com/docs/cli/)
- [RFC 9110 Content Negotiation](https://www.rfc-editor.org/rfc/rfc9110#name-content-negotiation)
