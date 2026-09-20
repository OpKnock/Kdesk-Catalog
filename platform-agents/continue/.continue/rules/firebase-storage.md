---
name: "Firebase Storage"
description: "Upload, download, delete, and secure files in it buckets. uploads.'"
globs: ["**/*.go", "**/*.java", "**/*.json", "**/*.r", "**/*.sh", "**/*.{js,ts,jsx,tsx}"]
alwaysApply: false
---

# Firebase Storage

Upload, download, delete, and secure files in it buckets. uploads.'

## Instructions

# Firebase Storage

## What this skill does

Firebase Storage stores user-generated files on Google Cloud Storage behind Firebase rules. gsutil/gcloud manage the bucket; storage.rules control read/write access.

## When to use

- Setting up file uploads for an app
- Cleaning up orphaned uploads
- Adding CORS so browsers can upload directly

## Real commands

```bash
# Deploy rules
firebase deploy --only storage:rules

# Manage objects
 gsutil ls gs://project.appspot.com/uploads/
 gsutil cp local-file gs://project.appspot.com/uploads/file1
 gsutil rm -r gs://project.appspot.com/uploads/

# CORS for web uploads
 gcloud storage cors set cors.json gs://project.appspot.com
```

## storage.rules example

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /uploads/{userId}/{file} {
      allow read: if request.auth != null;
      allow write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

## cors.json example

```json
[
  {
    "origin": ["https://myapp.example.com"],
    "method": ["GET", "PUT", "POST"],
    "maxAgeSeconds": 3600,
    "responseHeader": ["Content-Type", "x-goog-meta-*", "x-firebase-storage-version"]
  }
]
```

## Testing

```bash
# Verify rules deny unauthenticated writes
curl -s -o /dev/null -w '%{http_code}' -X PUT -F 'file=@x' 'https://firebasestorage.googleapis.com/v0/b/project.appspot.com/o/uploads%2Fanon%2Ffile'
```

## Best practices

- Keep user files under /uploads/{uid}/ paths enforced by rules.
- Set lifecycle rules in GCS to expire temp/derived objects.
- Never grant broad write access to the whole bucket.
- Test CORS changes with curl OPTIONS requests.
- Use resumable uploads for large files from clients.

## Capabilities

### storage-ops
Upload, download, delete, and secure files in Firebase Storage buckets.

**Commands:**
- `firebase deploy --only storage:rules`
- `gsutil ls gs://project.appspot.com/`
- `gsutil cp local-file gs://project.appspot.com/uploads/file1`
- `gsutil rm -r gs://project.appspot.com/uploads/`
- `gcloud storage cors set cors.json gs://project.appspot.com`

**Examples:**
- gsutil cp local-file gs://project.appspot.com/uploads/file1
- gsutil ls gs://project.appspot.com/uploads/
- gcloud storage cors set cors.json gs://project.appspot.com