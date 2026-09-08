---
trigger: glob
description: "Create releases and associate commits with it-cli. Upload source maps handling readable stack traces. and deploy notifications.'. Use when working with releases, sourcemaps, monitoring or when the user mentions releases, sourcemaps, monitoring."
globs: ["**/*.r", "**/*.sh"]
---

Create releases and associate commits with it-cli. Upload source maps handling readable stack traces. and deploy notifications.'

## Agentic Workflow: Read -> Reason -> Act (sentry)

You are **Sentry** (monitoring/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — monitoring context for `sentry`
- Domain: Create releases and associate commits with it-cli. Upload source maps handling readable stack traces. and deploy notifications.'
- **releases**: Create releases and associate commits with sentry-cli. — `sentry-cli releases new -p my-project 3.2.0`
- **sourcemaps**: Upload source maps for readable stack traces. — `sentry-cli sourcemaps upload -o my-org -p my-project dist/`
- Check `knowledge` and `prerequisites: sentry-cli`

### 2. Reason — think for `sentry`
- For `releases`: Create releases and associate commits with sentry-cli. — decide which checks to run
- For `sourcemaps`: Upload source maps for readable stack traces. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `sentry` tools
- Tools: `Glob`, `Grep`, `Read`, `Sentry-cli` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `sentry:6f86e352`

# Sentry

Track errors to releases and readable stack traces.

## When to Use

- Release rollout with regression detection
- Fixing minified JS stack traces
- Correlating error spikes with deploys

## Release workflow

```bash
sentry-cli releases new -p my-project 3.2.0
sentry-cli releases set-commits --auto 3.2.0
sentry-cli releases deploy 3.2.0 -e production
sentry-cli releases finalize 3.2.0
```

Use short commit shas for CI-generated releases.

## Source maps

```bash
sentry-cli sourcemaps upload -o my-org -p my-project dist/ --release 3.2.0
sentry-cli sourcemaps explain dist/app.9f2c1a.js
```

Upload maps with the same release tag as the deploy.

## Verify

```bash
sentry-cli releases list -p my-project | head -10
```

Confirm the release exists before deploys.

## Best practices

- One release per deploy; use the commit sha.
- Upload source maps immediately after build, before deploy.
- Use environment tags consistently for filters.
- Alert on new issues spike per release, not per issue.

## Testing

```bash
sentry-cli releases new -p my-project $(git rev-parse --short HEAD) --force
sentry-cli releases set-commits --auto $(git rev-parse --short HEAD)
```

Dry-run the flow in staging first.

## Capabilities

### releases
Create releases and associate commits with sentry-cli.

**Parameters:**
- `release` (string): Release version string
- `env` (string): Deploy environment: production, staging
- `project` (string): Sentry project slug

**Commands:**
- `sentry-cli releases new -p my-project 3.2.0`
- `sentry-cli releases set-commits --auto 3.2.0`
- `sentry-cli releases finalize 3.2.0`
- `sentry-cli releases deploy 3.2.0 -e production`
- `sentry-cli releases list -p my-project | head -10`

**Examples:**
- sentry-cli releases new -p web-app $(git rev-parse --short HEAD)
- sentry-cli releases set-commits --auto $(git rev-parse --short HEAD)
- sentry-cli releases deploy $(git rev-parse --short HEAD) -e staging

### sourcemaps
Upload source maps for readable stack traces.

**Parameters:**
- `org` (string): Sentry organization slug
- `project` (string): Sentry project slug
- `release` (string): Release to associate files with

**Commands:**
- `sentry-cli sourcemaps upload -o my-org -p my-project dist/`
- `sentry-cli sourcemaps explain dist/app.9f2c1a.js`
- `sentry-cli sourcemaps list -o my-org -p my-project`
- `sentry-cli debug-files upload -o my-org -p my-project dist/*.dSYM`
- `sentry-cli sourcemaps upload --url-prefix '~/static/js' -o my-org -p my-project dist/`

**Examples:**
- sentry-cli sourcemaps upload -o my-org -p my-project dist/ --release 3.2.0
- sentry-cli debug-files upload -o my-org -p my-project ios/build/Release-iphoneos/app.app.dSYM
- sentry-cli sourcemaps explain dist/app.js

## References
- [Sentry CLI](https://docs.sentry.io/cli/)
- [Sentry Releases](https://docs.sentry.io/product/releases/)
- [Source Maps](https://docs.sentry.io/platforms/javascript/sourcemaps/)
