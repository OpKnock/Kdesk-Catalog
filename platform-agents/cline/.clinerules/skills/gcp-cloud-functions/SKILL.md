---
name: "gcp-cloud-functions"
description: "Deploy and manage Cloud Functions (Gen2): deploy from source, set env vars, view logs, and invoke functions for testing. Use when working with gcf deploy, api or when the user mentions gcf deploy, api."
license: "MIT"
compatibility: "Requires gcloud."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(gcloud:*)"
---

Deploy and manage Cloud Functions (Gen2): deploy from source, set env vars, view logs, and invoke functions for testing.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `gcloud functions deploy orders-processor --runtime=nodejs20 `
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

# GCP Cloud Functions

## What this skill does

Cloud Functions runs single-purpose serverless functions triggered by HTTP, Pub/Sub, storage, or schedules. Gen2 functions run on Cloud Run infrastructure with more scaling control.

## When to use

- Event-driven glue: process a message, resize an image, webhook handler
- Cheap scaling for variable workloads
- Prototyping serverless quickly

## Real commands

```bash
# HTTP function
 gcloud functions deploy hello --runtime=python312 --trigger-http --allow-unauthenticated --gen2

# Pub/Sub-triggered function
 gcloud functions deploy orders-processor --runtime=nodejs20 --trigger-topic=orders --region=us-central1 --gen2

# Invoke and read logs
 gcloud functions call orders-processor --region=us-central1 --data='{"orderId":"1"}'
 gcloud functions logs read orders-processor --region=us-central1 --limit=20

# Get the URL
 gcloud functions describe orders-processor --region=us-central1 --format='value(serviceConfig.uri)'
```

## Env vars and retries

```bash
 gcloud functions deploy orders-processor --set-env-vars=DB_URL=postgres://... --max-retries=3 --gen2
```

## Testing

```bash
# Direct HTTP invocation
URL=$(gcloud functions describe hello --region=us-central1 --gen2 --format='value(serviceConfig.uri)')
curl -s -X POST "$URL" -H 'Content-Type: application/json' -d '{"msg":"ping"}'
```

## Best practices

- Make functions idempotent; Pub/Sub may retry delivery.
- Set `--max-retries` deliberately (0 for fire-and-forget).
- Keep cold starts low: minimal dependencies, no heavy init.
- Use env vars via `--set-env-vars`, never secrets in source.
- Use secrets via Secret Manager references for credentials.

## Capabilities

### gcf-deploy
Deploy, invoke, log, and configure Cloud Functions.

**Parameters:**
- `function-name` (string): Function name to deploy
- `runtime` (string): nodejs20, python312, go122
- `trigger` (string): http, topic, bucket, or schedule trigger

**Commands:**
- `gcloud functions deploy orders-processor --runtime=nodejs20 --trigger-topic=orders --region=us-central1 --gen2`
- `gcloud functions deploy hello --runtime=python312 --trigger-http --allow-unauthenticated --gen2`
- `gcloud functions call orders-processor --region=us-central1 --data='{"orderId":"1"}'`
- `gcloud functions logs read orders-processor --region=us-central1 --limit=20`
- `gcloud functions describe orders-processor --region=us-central1 --format='value(serviceConfig.uri)'`
- `gcloud functions delete orders-processor --region=us-central1 --quiet`

**Examples:**
- gcloud functions deploy hello --runtime=python312 --trigger-http --allow-unauthenticated --gen2
- gcloud functions call orders-processor --region=us-central1 --data='{"orderId":"1"}'
- gcloud functions logs read orders-processor --region=us-central1 --limit=20

## References
- [Cloud Functions docs](https://cloud.google.com/functions/docs)
- [gcloud functions reference](https://cloud.google.com/sdk/gcloud/reference/functions)
