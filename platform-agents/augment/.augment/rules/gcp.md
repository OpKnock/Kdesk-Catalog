---
type: agent_requested
description: "Operates Google Cloud with the gcloud CLI: compute, GKE, Cloud Run, gsutil, IAM, and service accounts. Use when working with gcp core, gcp run, gcp gke, cloud or when the user mentions gcp core, gcp run, gcp gke, cloud."
---

Operates Google Cloud with the gcloud CLI: compute, GKE, Cloud Run, gsutil, IAM, and service accounts.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `gcloud auth login`, `gcloud run deploy myapp --image gcr.io/my-project/myapp:1.0 `
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

# Google Cloud

Operate GCP with the gcloud CLI.

## When to Use

- Compute and GKE cluster management
- Cloud Run serverless deploys
- Cloud Storage via gsutil
- IAM and service account management

## Commands

```bash
# Auth and project
gcloud auth login
gcloud config set project my-project
gcloud projects list

# Compute
gcloud compute instances list
gcloud compute instances describe my-instance --zone us-central1-a

# Storage
gsutil ls
gsutil cp file.txt gs://my-bucket/

# Cloud Run
gcloud builds submit --tag gcr.io/my-project/myapp:1.0
gcloud run deploy myapp --image gcr.io/my-project/myapp:1.0 \
  --region us-central1 --allow-unauthenticated
gcloud run services describe myapp --region us-central1
gcloud run services update-traffic myapp --to-latest --region us-central1

# GKE
gcloud container clusters create mycluster --zone us-central1-a --num-nodes 3
gcloud container clusters get-credentials mycluster --zone us-central1-a
kubectl get nodes
```

## Best Practices

- Use gcloud config set project to avoid cross-project mistakes
- Prefer Workload Identity over static service account keys
- Grant minimum roles; use IAM conditions where possible
- Pin container tags; avoid :latest in production
- Use --allow-unauthenticated only for public services
- Enable logging and check Cloud Logging for errors

## Capabilities

### gcp-core
Manage projects, compute, and storage.

**Parameters:**
- `project` (string): GCP project id
- `zone` (string): Compute zone

**Commands:**
- `gcloud auth login`
- `gcloud config set project my-project`
- `gcloud compute instances list`
- `gsutil ls`
- `gcloud projects list`

**Examples:**
- gcloud config list
- gsutil cp file.txt gs://my-bucket/
- gcloud compute instances describe my-instance --zone us-central1-a

### gcp-run
Deploy and manage Cloud Run services.

**Parameters:**
- `service` (string): Cloud Run service name
- `image` (string): Container image reference

**Commands:**
- `gcloud run deploy myapp --image gcr.io/my-project/myapp:1.0 --region us-central1 --allow-unauthenticated`
- `gcloud run services list`
- `gcloud run services describe myapp --region us-central1`
- `gcloud run services update-traffic myapp --to-latest --region us-central1`
- `gcloud builds submit --tag gcr.io/my-project/myapp:1.0`

**Examples:**
- gcloud run deploy myapp --image gcr.io/my-project/myapp:1.0 --region us-central1 --min-instances 1
- gcloud run services update-traffic myapp --to-revisions REVISION=50 --region us-central1

### gcp-gke
Manage GKE clusters and kubectl context.

**Parameters:**
- `cluster` (string): GKE cluster name
- `zone` (string): Compute zone

**Commands:**
- `gcloud container clusters create mycluster --zone us-central1-a --num-nodes 3`
- `gcloud container clusters get-credentials mycluster --zone us-central1-a`
- `gcloud container clusters list`
- `kubectl get nodes`

**Examples:**
- gcloud container clusters resize mycluster --node-pool default-pool --num-nodes 5
- gcloud container node-pools list --cluster mycluster

## References
- [gcloud CLI Reference](https://cloud.google.com/sdk/gcloud/reference/)
- [Cloud Run Docs](https://cloud.google.com/run/docs)