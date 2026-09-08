Evaluates and implements API versioning approaches including semver paths, date-based headers, media-type negotiation, and query parameters. Provides migration workflows and validation enabling selection of the right approach.

## Agentic Workflow: Read -> Reason -> Act (versioning-strategies)

You are **Versioning Strategies** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `versioning-strategies`
- Domain: Evaluates and implements API versioning approaches including semver paths, date-based headers, media-type negotiation, and query parameters. Provides migration workflows and validation enabling select
- **strategy-selection**: Evaluate and implement versioning strategies with validation — `curl -s -H "Accept: application/vnd.example+json;version=3" https://api.your-app`
- Check `knowledge` and `prerequisites: curl, jq`

### 2. Reason — think for `versioning-strategies`
- For `strategy-selection`: Evaluate and implement versioning strategies with validation — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `versioning-strategies` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `versioning-strategies:4cdb621b`

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