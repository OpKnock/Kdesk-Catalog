---
name: "gcp-secret-manager"
description: "Store and manage secrets in GCP Secret Manager: create and version secrets, access values, and grant access via IAM. Use when working with secret manager, api or when the user mentions secret manager, api."
type: knowledge
triggers: ["gcp-secret-manager", "secret-manager"]
---

Store and manage secrets in GCP Secret Manager: create and version secrets, access values, and grant access via IAM.

## Agentic Workflow: Read -> Reason -> Act (gcp-secret-manager)

You are **Gcp Secret Manager** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `gcp-secret-manager`
- Domain: Store and manage secrets in GCP Secret Manager: create and version secrets, access values, and grant access via IAM.
- **secret-manager**: Create, access, version, and delete secrets with gcloud. — `printf 'postgres://app:pass@db:5432/app' | gcloud secrets versions add db-url --`
- Check `knowledge` and `prerequisites: gcloud, printf`

### 2. Reason — think for `gcp-secret-manager`
- For `secret-manager`: Create, access, version, and delete secrets with gcloud. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `gcp-secret-manager` tools
- Tools: `Glob`, `Grep`, `Read`, `Printf`, `Gcloud` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `gcp-secret-manager:5ce12b35`

# GCP Secret Manager

## What this skill does

Secret Manager stores secrets (API keys, DB passwords) with versioning and fine-grained IAM. Cloud Run/Functions reference secrets by version without embedding values.

## When to use

- Centralizing credentials that many services need
- Versioned rotation without coordinated deploys
- Passing secrets to serverless via env references

## Real commands

```bash
# Create a secret from stdin
printf 'postgres://app:pass@db:5432/app' | gcloud secrets create db-url --replication-policy=automatic --data-file=-

# Add a version
printf 'postgres://app:newpass@db:5432/app' | gcloud secrets versions add db-url --data-file=-

# Access and list versions
 gcloud secrets versions access latest --secret=db-url
 gcloud secrets versions list db-url

# Destroy a version (30-day grace for restore)
 gcloud secrets versions destroy 2 --secret=db-url

# Grant access to a service account
 gcloud secrets add-iam-policy-binding db-url --member=serviceAccount:app-sa@my-project.iam.gserviceaccount.com --role=roles/secretmanager.secretAccessor
```

## Cloud Run reference

```bash
 gcloud run services update orders --region=us-central1 --set-secrets=DB_URL=db-url:latest
```

## Testing

```bash
# Verify the value round trips
V=$(gcloud secrets versions access latest --secret=db-url)
test "$V" = "$EXPECTED" && echo OK
```

## Best practices

- Never copy secret values into chat, logs, or gist.
- Reference secrets by version for serverless; use latest only for rotation windows.
- Rotate with a new version, then destroy old ones after the grace period.
- Grant least privilege: secretAccessor per service account per secret.
- Enable automatic replication for HA; user-managed for compliance pinning.

## Capabilities

### secret-manager
Create, access, version, and delete secrets with gcloud.

**Parameters:**
- `secret-name` (string): Secret identifier
- `version` (string): Version number or latest
- `replication` (string): automatic or user-managed replication

**Commands:**
- `printf 'postgres://app:pass@db:5432/app' | gcloud secrets versions add db-url --data-file=-`
- `gcloud secrets create db-url --replication-policy=automatic --data-file=- <<< 'postgres://...'`
- `gcloud secrets versions access latest --secret=db-url`
- `gcloud secrets versions list db-url`
- `gcloud secrets versions destroy latest --secret=db-url`
- `gcloud secrets add-iam-policy-binding db-url --member=serviceAccount:app-sa@my-project.iam.gserviceaccount.com --role=roles/secretmanager.secretAccessor`

**Examples:**
- gcloud secrets versions access latest --secret=db-url
- gcloud secrets create db-url --replication-policy=automatic --data-file=- <<< 'postgres://...'
- gcloud secrets add-iam-policy-binding db-url --member=serviceAccount:app-sa@my-project.iam.gserviceaccount.com --role=roles/secretmanager.secretAccessor

## References
- [Secret Manager docs](https://cloud.google.com/secret-manager/docs)
- [gcloud secrets reference](https://cloud.google.com/sdk/gcloud/reference/secrets)
