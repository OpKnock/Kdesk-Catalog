---
name: "gcp-cloud-run"
description: "Deploy and operate containers on Cloud Run: deploy revisions, configure scaling and env vars, manage traffic splits, and view logs. Use when working with cloud run, api or when the user mentions cloud run, api."
---

Deploy and operate containers on Cloud Run: deploy revisions, configure scaling and env vars, manage traffic splits, and view logs.

## Agentic Workflow: Read -> Reason -> Act (gcp-cloud-run)

You are **Gcp Cloud Run** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `gcp-cloud-run`
- Domain: Deploy and operate containers on Cloud Run: deploy revisions, configure scaling and env vars, manage traffic splits, and view logs.
- **cloud-run**: Deploy revisions, manage traffic, scale, and configure Cloud Run services. — `gcloud run deploy orders --image=gcr.io/my-project/orders:v1.2.3 --region=us-cen`
- Check `knowledge` and `prerequisites: gcloud`

### 2. Reason — think for `gcp-cloud-run`
- For `cloud-run`: Deploy revisions, manage traffic, scale, and configure Cloud Run services. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `gcp-cloud-run` tools
- Tools: `Glob`, `Grep`, `Read`, `Gcloud` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `gcp-cloud-run:310fa0e2`

# GCP Cloud Run

## What this skill does

Cloud Run runs stateless containers on a serverless platform that scales to zero. Every deploy creates a revision; traffic can be split across revisions for canary releases.

## When to use

- Deploying containerized APIs without managing servers
- Canary releases via traffic splitting
- Autoscaling webhooks and batch jobs

## Real commands

```bash
# Deploy a revision
 gcloud run deploy orders --image=gcr.io/my-project/orders:v1.2.3 --region=us-central1 --allow-unauthenticated

# Get the URL
 gcloud run services describe orders --region=us-central1 --format='value(status.url)'

# Canary: 10% to new revision
 gcloud run services update-traffic orders --region=us-central1 --to-revisions=orders-00001=10,orders-00002=90

# Scaling and env
 gcloud run services update orders --region=us-central1 --min-instances=1 --max-instances=20 --set-env-vars=LOG_LEVEL=info

# Logs
 gcloud run services logs read orders --region=us-central1 --limit=50
```

## Rollback

```bash
# Return all traffic to the previous revision
 gcloud run services update-traffic orders --region=us-central1 --to-latest
```

## Testing

```bash
# Warm the container and check headers
curl -sI "$(gcloud run services describe orders --region=us-central1 --format='value(status.url)')/health" | grep -i 'HTTP'
```

## Best practices

- Use `--no-allow-unauthenticated` for internal services and add IAM.
- Set `--max-instances` to cap cold-start and cost spikes.
- Deploy immutable tags (v1.2.3) so revisions are identifiable.
- Split traffic 10% and watch metrics before full rollout.
- Use Secret Manager env references for credentials.

## Capabilities

### cloud-run
Deploy revisions, manage traffic, scale, and configure Cloud Run services.

**Parameters:**
- `service` (string): Cloud Run service name
- `image` (string): Container image reference
- `revision-traffic` (string): Traffic split spec like rev1=50,rev2=50

**Commands:**
- `gcloud run deploy orders --image=gcr.io/my-project/orders:v1.2.3 --region=us-central1 --allow-unauthenticated`
- `gcloud run services describe orders --region=us-central1 --format='value(status.url)'`
- `gcloud run services update-traffic orders --region=us-central1 --to-revisions=orders-00001=10,orders-00002=90`
- `gcloud run services update orders --region=us-central1 --min-instances=1 --max-instances=20 --set-env-vars=LOG_LEVEL=info`
- `gcloud run revisions list --service=orders --region=us-central1`
- `gcloud run services logs read orders --region=us-central1 --limit=50`

**Examples:**
- gcloud run deploy orders --image=gcr.io/my-project/orders:v1.2.3 --region=us-central1 --allow-unauthenticated
- gcloud run services update-traffic orders --region=us-central1 --to-revisions=orders-00001=10,orders-00002=90
- gcloud run services describe orders --region=us-central1 --format='value(status.url)'

## References
- [Cloud Run docs](https://cloud.google.com/run/docs)
- [gcloud run reference](https://cloud.google.com/sdk/gcloud/reference/run)
