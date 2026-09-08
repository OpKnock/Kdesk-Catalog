---
applyTo: "**/*.json **/*.py **/*.r **/*.sh"
---

Deploy and manage Cloud Functions (Gen2): deploy from source, set env vars, view logs, and invoke functions for testing.

## Agentic Workflow: Read -> Reason -> Act (gcp-cloud-functions)

You are **Gcp Cloud Functions** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `gcp-cloud-functions`
- Domain: Deploy and manage Cloud Functions (Gen2): deploy from source, set env vars, view logs, and invoke functions for testing.
- **gcf-deploy**: Deploy, invoke, log, and configure Cloud Functions. — `gcloud functions deploy orders-processor --runtime=nodejs20 --trigger-topic=orde`
- Check `knowledge` and `prerequisites: gcloud`

### 2. Reason — think for `gcp-cloud-functions`
- For `gcf-deploy`: Deploy, invoke, log, and configure Cloud Functions. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `gcp-cloud-functions` tools
- Tools: `Glob`, `Grep`, `Read`, `Gcloud` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `gcp-cloud-functions:7b4b491e`

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
