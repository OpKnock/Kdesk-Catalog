---
trigger: glob
description: "Evaluates and implements API versioning approaches including semver paths, date-based headers, media-type negotiation, and query parameters. Provides migration workflows and validation enabling selection of the right approach. Use when working with strategy selection, api, versioning, architecture or when the user mentions strategy selection, api, versioning, architecture."
globs: ["**/*.go", "**/*.json", "**/*.r", "**/*.sh"]
---

Evaluates and implements API versioning approaches including semver paths, date-based headers, media-type negotiation, and query parameters. Provides migration workflows and validation enabling selection of the right approach.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -s -H "Accept: application/vnd.example+json;version=3" `
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

# Versioning Strategies

## What this skill does

Help teams choose and implement an API versioning strategy. Compares semver paths (/v2), date-based
headers (X-Version), media-type negotiation (Accept), and query params, including migration and validation
workflows.

## When to use

- Selecting a strategy for a new product API
- Migrating from path versioning to header versioning
- Auditing an inconsistent versioning scheme

## Strategy comparison

| Strategy | Pros | Cons |
|---|---|---|
| URI path /v2 | Explicit, cacheable, debuggable | Pollutes URLs |
| Date header | No URL change, natural timeline | Easy to forget |
| Media type | Per-resource versions | Complex tooling |
| Query param | Simple | Poor cache keys |

## Real commands

```bash
# Media-type negotiation
curl -s -H "Accept: application/vnd.example+json;version=3" https://api.your-app.test/widgets

# Date-based header
curl -s -H "X-Version: 2024-06-01" https://api.your-app.test/widgets | jq ".version"

# Query param
curl -s "https://api.your-app.test/widgets?version=3.0" | jq ".data[0]"

# Deprecated version still served?
curl -sI https://api.your-app.test/widgets -H "Accept: application/vnd.example+json;version=1" | grep -i sunset

# Latency comparison across versions
curl -s https://api.your-app.test/v3/widgets -o /dev/null -w "%{time_total}s\n"
curl -s "https://api.your-app.test/widgets?version=1" -o /dev/null -w "%{time_total}s\n"
```

## Migration workflow

1. Ship the new version alongside the old one
2. Serve both for at least one deprecation cycle
3. Emit Deprecation + Sunset headers on the old version
4. Migrate consumers, then remove the old version

## Best practices

- Pick one primary strategy; do not mix path and query versioning
- For SaaS APIs, prefer date-based headers with per-customer pinning
- Test the default (unversioned) request returns the latest version

## Testing

```bash
for v in 1 2 3; do curl -s -H "X-Version: 2024-0$v-01" https://api.your-app.test/widgets -o /dev/null -w "v$v: %{http_code}\n"; done
```

## Capabilities

### strategy-selection
Evaluate and implement versioning strategies with validation

**Parameters:**
- `version` (string): Version in Accept-Version header or query param
- `sunset` (string): Retirement date returned in Sunset header

**Commands:**
- `curl -s -H "Accept: application/vnd.example+json;version=3" https://api.your-app.test/widgets`
- `curl -s -H "X-Version: 2024-06-01" https://api.your-app.test/widgets | jq ".version"`
- `curl -s "https://api.your-app.test/widgets?version=3.0" | jq ".data[0]"`
- `curl -sI https://api.your-app.test/widgets -H "Accept: application/vnd.example+json;version=1" | grep -i sunset`
- `curl -s https://api.your-app.test/v3/widgets -o /dev/null -w "%{time_total}s"`

**Examples:**
- curl -s -H "Accept: application/vnd.example+json;version=2" https://api.your-app.test/widgets | jq ".schema"
- curl -s -D - -o /dev/null -H "Accept-Version: 1" https://api.your-app.test/widgets | grep -iE "^(HTTP|deprecation)"
- curl -s "https://api.your-app.test/widgets?version=2" | jq ".version"

## References
- [Stripe API Versioning](https://stripe.com/docs/api/versioning)
- [Swagger API Versioning Guide](https://swagger.io/resources/articles/software-versioning-in-swagger/)
- [Microsoft API Versioning](https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design)
