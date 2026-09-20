---
trigger: glob
description: "Store and manage secrets in GCP Secret Manager: create and version secrets, access values, and grant access via IAM."
globs: ["**/*.r", "**/*.sh"]
---

# Gcp Secret Manager

Store and manage secrets in GCP Secret Manager: create and version secrets, access values, and grant access via IAM.

## Instructions

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
