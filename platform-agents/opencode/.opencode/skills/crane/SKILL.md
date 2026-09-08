---
name: "crane"
description: "Manipulates container images and registries with google/crane: copy, move, tag, export, and validate image manifests and digests. Use when working with registry operations, manifest and digest, devops or when the user mentions registry operations, manifest and digest, devops."
---

Manipulates container images and registries with google/crane: copy, move, tag, export, and validate image manifests and digests.

## Agentic Workflow: Read -> Reason -> Act (crane)

You are **crane** (devops/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devops context for `crane`
- Domain: Manipulates container images and registries with google/crane: copy, move, tag, export, and validate image manifests and digests.
- **registry-operations**: Copy, move, tag, and delete images across registries without a full daemon. — `crane copy nginx:latest ghcr.io/nginx:latest`
- **manifest-and-digest**: Inspect manifests, digests, and export images for offline analysis. — `crane manifest nginx:latest | jq .`
- Check `knowledge` and `prerequisites: crane`

### 2. Reason — think for `crane`
- For `registry-operations`: Copy, move, tag, and delete images across registries without a full daemon. — decide which checks to run
- For `manifest-and-digest`: Inspect manifests, digests, and export images for offline analysis. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `crane` tools
- Tools: `Glob`, `Grep`, `Read`, `Crane` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `crane:89c9bbcb`

# crane Registry Tooling

Copy, tag, and inspect container images across registries using google/crane — no daemon required.

## What This Skill Does

- Copies and moves images between registries (mirroring, air-gapped transfer)
- Reads OCI/Docker manifests and computes digests
- Exports images to tarballs for offline or malware analysis
- Validates images and lists tags/repos
- Auth to private registries with plain or credential helpers

## When to Use

- Mirroring images into a private registry
- Pinning digests for supply-chain safety
- Verifying that an image was not tampered with
- Air-gapped environments where `docker pull` is unavailable

## Real Commands

```bash
# Copy between registries
crane copy nginx:latest ghcr.io/nginx:latest
crane copy nginx:latest ghcr.io/nginx:latest -p     # preserve exact tag list

# Move / tag / delete
crane move old.example.com/app:v1 new.example.com/app:v1
crane tag nginx:latest v1.0.0
crane delete ghcr.io/app:v1

# Inspect
crane manifest nginx:latest
crane digest nginx:latest
crane ls ghcr.io/app
crane index ls ghcr.io/app

# Export and validate
crane export nginx:latest /tmp/nginx.tar
crane validate --remote --tarball /tmp/nginx.tar ghcr.io/app

# Auth
crane auth login ghcr.io -u user -p pass
```

## Best Practices

- Always pin images by digest in production (`image@sha256:...`)
- Use `crane validate --remote` in CI to catch broken images early
- Copy with `-p` when preserving tags matters (e.g. `latest`)
- Verify registry ACLs with `crane auth login` before large transfers

## Capabilities

### registry-operations
Copy, move, tag, and delete images across registries without a full daemon.

**Parameters:**
- `src` (string): Source image or repo reference
- `dest` (string): Destination repo reference
- `tag` (string): Tag to apply

**Commands:**
- `crane copy nginx:latest ghcr.io/nginx:latest`
- `crane move old.example.com/app:v1 new.example.com/app:v1`
- `crane tag nginx:latest v1.0.0`
- `crane delete ghcr.io/app:v1`
- `crane ls ghcr.io/app`
- `crane validate --remote ghcr.io/app`

**Examples:**
- crane copy nginx:latest ghcr.io/nginx:latest
- crane tag nginx:latest v1.0.0
- crane ls ghcr.io/app

### manifest-and-digest
Inspect manifests, digests, and export images for offline analysis.

**Parameters:**
- `image` (string): Image reference to inspect
- `output` (string): Output tar file for export

**Commands:**
- `crane manifest nginx:latest | jq .`
- `crane digest nginx:latest`
- `crane export nginx:latest nginx.tar`
- `crane index ls ghcr.io/app`
- `crane auth login ghcr.io -u user -p pass`

**Examples:**
- crane digest nginx:latest
- crane export nginx:latest /tmp/nginx.tar
- crane manifest nginx:latest | jq -r .mediaType

## References
- [crane CLI Reference](https://github.com/google/go-containerregistry/blob/main/cmd/crane/README.md)
- [go-containerregistry Project](https://github.com/google/go-containerregistry)
