---
trigger: glob
description: "Builds OCI container images without a daemon using buildah: containerfiles, commits, and pushes."
globs: ["**/*.r", "**/*.sh", "**/Dockerfile*"]
---

# buildah

Builds OCI container images without a daemon using buildah: containerfiles, commits, and pushes.

## Instructions

# Buildah

Builds OCI images without a daemon and without root for many workflows: handy for
CI where Docker isn't available.

## When to Use

- Building images in rootless CI environments
- Fine-grained image creation from the CLI
- Replacing docker build in daemon-less hosts

## Real Commands

```bash
# Build from a Containerfile
sudo buildah bud -t myapp:latest .
sudo buildah bud -f Containerfile.dev -t myapp:dev --layers .

# Manual image construction
ctr=$(sudo buildah from alpine:3.19)
sudo buildah run $ctr -- sh -c "apk add --no-cache curl"
sudo buildah config --entrypoint '["/usr/bin/myapp"]' $ctr
sudo buildah commit $ctr myimage:v1

# Inspect
sudo buildah images
sudo buildah inspect myimage:v1

# Push
sudo buildah push myimage:v1 quay.io/org/myimage:v1

# Cleanup
sudo buildah rm -a
sudo buildah rmi -a
```

## Containerfile Example

```dockerfile
FROM alpine:3.19
RUN apk add --no-cache curl
COPY app /usr/bin/app
ENTRYPOINT ["/usr/bin/app"]
```

## Best Practices

- Prefer `buildah bud` from a committed Containerfile
- Use `--layers` to reuse cache in CI
- Set labels and entrypoint via buildah config
- Combine buildah push with skopeo for cross-repo copies
- Clean up build containers in CI to avoid leaks

## Example Response

Builds the image, verifies it with inspect, pushes it, and cleans up the
intermediate build containers.

## Capabilities

### buildah-images
Create, modify, commit, and push container images

**Commands:**
- `buildah bud -t myapp:latest .`
- `buildah from alpine:3.19`
- `buildah run container1 -- sh -c "apk add --no-cache curl"`
- `buildah commit container1 myimage:v1`
- `buildah push myimage quay.io/org/myimage:v1`

**Examples:**
- buildah bud -f Containerfile.dev -t myapp:dev .
- buildah images
- buildah rm -a && buildah rmi -a
