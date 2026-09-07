---
applyTo: "**/*.r **/*.sh"
---

Deploy and operate containers on Cloud Run: deploy revisions, configure scaling and env vars, manage traffic splits, and view logs.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `gcloud run deploy orders --image=gcr.io/my-project/orders:v1`
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
