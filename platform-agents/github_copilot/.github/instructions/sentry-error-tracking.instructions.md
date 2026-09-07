---
applyTo: "**/*.json **/*.py **/*.r **/*.sh"
---

Operates Sentry end-to-end: bootstraps the Python SDK with DSN and release context, manages releases and deploys via sentry-cli with commit linking, and verifies the ingest pipeline with raw envelope submissions.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `pip install sentry-sdk`
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
