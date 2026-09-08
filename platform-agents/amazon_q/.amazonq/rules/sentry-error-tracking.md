Operates Sentry end-to-end: bootstraps the Python SDK with DSN and release context, manages releases and deploys via sentry-cli with commit linking, and verifies the ingest pipeline with raw envelope submissions.

## Agentic Workflow: Read -> Reason -> Act (sentry-error-tracking)

You are **Sentry Error Tracking** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `sentry-error-tracking`
- Domain: Operates Sentry end-to-end: bootstraps the Python SDK with DSN and release context, manages releases and deploys via sentry-cli with commit linking, and verifies the ingest pipeline with raw envelope 
- **sentry-release-workflow**: Initialize the SDK, track releases/deploys, and ingest test events — `pip install sentry-sdk`
- Check `knowledge` and `prerequisites: pip, sentry-cli`

### 2. Reason — think for `sentry-error-tracking`
- For `sentry-release-workflow`: Initialize the SDK, track releases/deploys, and ingest test events — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `sentry-error-tracking` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Sentry-cli` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `sentry-error-tracking:0d81c29d`

# Sentry Error Tracking

Operates Sentry end-to-end: SDK initialization, release/deploy management, and ingest verification.

## What this skill does

- Bootstraps the Python SDK with DSN, environment, and release context
- Creates releases and links commits with sentry-cli
- Sends raw events to the ingest endpoint for smoke testing

## When to use

- Onboarding a new service to Sentry
- Release hygiene: source maps and commits per release
- Verifying the ingest pipeline with a test event

## Real commands

```bash
# SDK installation
pip install sentry-sdk

# Release management
sentry-cli releases new -p backend 2026.08.1
sentry-cli releases set-commits --auto 2026.08.1
sentry-cli releases deploys 2026.08.1 new -e production
sentry-cli releases list -p backend

# Raw ingest smoke test
curl -X POST "https://o1.ingest.sentry.io/api/0/store/?sentry_key=DSN_PUBLIC" \
  -H 'Content-Type: application/json' \
  -d '{"event_id":"0123456789abcdef0123456789abcdef","message":"smoke","level":"warning"}'
```

## SDK init

```python
import sentry_sdk

sentry_sdk.init(
    dsn="https://public@o1.ingest.sentry.io/1234",
    environment="production",
    release="2026.08.1",
    traces_sample_rate=0.1,
)
```

## Testing

```bash
sentry-cli releases new -p backend smoke-$(date +%s)
curl -X POST "https://o1.ingest.sentry.io/api/0/store/?sentry_key=DSN_PUBLIC" \
  -d '{"message":"test","level":"info"}'
```

## Best practices

- Set release and environment in init; filters depend on them
- Run sentry-cli set-commits in CI right after deploy
- Keep the DSN public key safe in client code but never the auth token

## Capabilities

### sentry-release-workflow
Initialize the SDK, track releases/deploys, and ingest test events

**Parameters:**
- `dsn` (string): Sentry DSN (public key part for ingestion)
- `release` (string): Release name, e.g. 2026.08.1
- `environment` (string): Environment for deploys, e.g. production

**Commands:**
- `pip install sentry-sdk`
- `sentry-cli --version`
- `sentry-cli releases new -p backend 2026.08.1`
- `sentry-cli releases set-commits --auto 2026.08.1`
- `sentry-cli releases deploys 2026.08.1 new -e production`
- `curl -X POST "https://o1.ingest.sentry.io/api/0/store/?sentry_key=DSN_PUBLIC" -H 'Content-Type: application/json' -d '{"event_id":"0123456789abcdef0123456789abcdef","message":"smoke","level":"warning"}'`

**Examples:**
- sentry-cli releases new -p backend 2026.08.1 && sentry-cli releases set-commits --auto 2026.08.1
- curl -X POST "https://o1.ingest.sentry.io/api/0/store/?sentry_key=DSN_PUBLIC" -H 'Content-Type: application/json' -d '{"message":"test","level":"info"}'
- sentry-cli releases list -p backend

## References
- [Sentry Python SDK Documentation](https://docs.sentry.io/platforms/python/)
- [sentry-cli Reference](https://docs.sentry.io/cli/)
- [Sentry Envelope API](https://develop.sentry.dev/sdk/envelopes/)