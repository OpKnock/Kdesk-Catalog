---
type: agent_requested
description: "Inspects, copies, and signs container images with skopeo \u2014 registry operations without a daemon, including sync and list-tags. Use when working with image inspection, copy and sync, devops or when the user mentions image inspection, copy and sync, devops."
---

Inspects, copies, and signs container images with skopeo — registry operations without a daemon, including sync and list-tags.

## Agentic Workflow: Read -> Reason -> Act (skopeo)

You are **skopeo** (devops/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devops context for `skopeo`
- Domain: Inspects, copies, and signs container images with skopeo — registry operations without a daemon, including sync and list-tags.
- **image-inspection**: Inspect images and registries without pulling layers locally. — `skopeo inspect docker://nginx:latest`
- **copy-and-sync**: Copy images between transports/registries and sync repositories. — `skopeo copy docker://nginx:latest docker://ghcr.io/nginx:latest`
- Check `knowledge` and `prerequisites: skopeo`

### 2. Reason — think for `skopeo`
- For `image-inspection`: Inspect images and registries without pulling layers locally. — decide which checks to run
- For `copy-and-sync`: Copy images between transports/registries and sync repositories. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `skopeo` tools
- Tools: `Glob`, `Grep`, `Read`, `Skopeo` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `skopeo:adeae137`

# skopeo Registry Operations

Inspect, copy, and sign images between registries without a container daemon.

## What This Skill Does

- Inspects image metadata (digest, config, layers) remotely
- Lists tags and copies multi-arch images
- Syncs whole repositories to air-gapped targets
- Deletes remote images and manages auth
- Works with docker://, oci:, dir:, docker-archive: transports

## When to Use

- Mirroring images into private registries
- CI where no daemon is available (common in hardened runners)
- Verifying image digests for supply chain audit

## Real Commands

```bash
# Inspect
skopeo inspect docker://nginx:latest
skopeo inspect --raw docker://nginx:latest | jq .
skopeo inspect --format '{{.Digest}}' docker://nginx:latest
skopeo list-tags docker://ghcr.io/app

# Copy
skopeo copy docker://nginx:latest docker://ghcr.io/nginx:latest
skopeo copy --all --preserve-digests docker://ghcr.io/org/app:1.0 docker://ghcr.io/org/app:1.0

# Sync to air gap
skopeo sync --src docker --dest dir nginx:latest /opt/images
skopeo sync --src yaml --dest docker sync.yaml

# Auth and delete
skopeo login ghcr.io -u ci -p $REGISTRY_PASS
skopeo delete docker://ghcr.io/old-app:v0.9
```

## Best Practices

- Use --all to preserve multi-arch manifests on copy
- Prefer --preserve-digests when mirroring to keep provenance
- Use `skopeo inspect --format '{{.Digest}}'` to pin digests in GitOps
- For air-gapped clusters, sync to dir transport, then load offline
- Scope CI credentials to pull-only on the source registry

## Capabilities

### image-inspection
Inspect images and registries without pulling layers locally.

**Parameters:**
- `image` (string): Image reference
- `format` (string): Go template for output

**Commands:**
- `skopeo inspect docker://nginx:latest`
- `skopeo inspect --raw docker://nginx:latest`
- `skopeo list-tags docker://ghcr.io/app`
- `skopeo inspect docker://ghcr.io/app:v1 --config`
- `skopeo inspect --format '{{.Digest}}' docker://nginx:latest`

**Examples:**
- skopeo inspect docker://nginx:latest
- skopeo list-tags docker://ghcr.io/app
- skopeo inspect --format '{{.Digest}}' docker://nginx:latest

### copy-and-sync
Copy images between transports/registries and sync repositories.

**Parameters:**
- `src` (string): Source image reference
- `dest` (string): Destination reference

**Commands:**
- `skopeo copy docker://nginx:latest docker://ghcr.io/nginx:latest`
- `skopeo copy --all --preserve-digests docker://ghcr.io/org/app:1.0 docker://ghcr.io/org/app:1.0`
- `skopeo sync --src docker --dest dir nginx:latest /opt/images`
- `skopeo delete docker://ghcr.io/old-app:v0.9`
- `skopeo login ghcr.io -u ci -p $(cat /run/secrets/registry)`

**Examples:**
- skopeo copy docker://nginx:latest docker://ghcr.io/nginx:latest
- skopeo sync --src docker --dest dir nginx:latest /opt/images
- skopeo delete docker://ghcr.io/old-app:v0.9

## References
- [skopeo GitHub](https://github.com/containers/skopeo)
- [containers-common Transports](https://github.com/containers/image/blob/main/docs/containers-transports.5.md)