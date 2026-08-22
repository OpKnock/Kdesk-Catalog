# hadolint

Lints Dockerfiles with hadolint: best-practice rules, shellcheck integration, and CI enforcement.

## Instructions

# Hadolint

Lint Dockerfiles for best practices.

## When to Use

- Enforcing minimal, safe images
- Catching apt-pin/apk-add without cleanup (DL30xx)
- CI gates on every Dockerfile change
- Checking for pinned versions and non-root users

## Commands

```bash
# Lint
hadolint Dockerfile

# Via docker (no local install)
docker run --rm -i hadolint/hadolint < Dockerfile

# Ignore rules
hadolint Dockerfile --ignore DL3007

# Failure threshold
hadolint Dockerfile --failure-threshold warning

# Formats
hadolint Dockerfile -f json
hadolint Dockerfile -f sarif -o hadolint.sarif

# Config file
hadolint Dockerfile --config .hadolint.yaml
```

## Config Example

```yaml
# .hadolint.yaml
failure-threshold: warning
ignored:
  - DL3007
trustedRegistries:
  - docker.io
```

## Best Practices

- Pin base image tags (DL3007 is untagged latest)
- Add --no-install-recommends and cleanup for apt
- Run as non-root (USER directive)
- Multi-stage builds for smaller images
- Run hadolint in CI with a JSON report
- Review rules before ignoring them; keep the list short

## Capabilities

### hadolint-lint
Lint Dockerfiles from CLI or stdin.

**Commands:**
- `hadolint Dockerfile`
- `hadolint Dockerfile --ignore DL3007`
- `hadolint Dockerfile --failure-threshold warning`
- `docker run --rm -i hadolint/hadolint < Dockerfile`
- `hadolint Dockerfile -f json`

**Examples:**
- hadolint Dockerfile.prod
- cat Dockerfile | hadolint -
- hadolint Dockerfile --trusted-registry docker.io --ignore DL3002

### hadolint-config
Manage rules and formats.

**Commands:**
- `hadolint --version`
- `hadolint Dockerfile --format sarif`
- `hadolint Dockerfile --no-color`
- `hadolint Dockerfile --config .hadolint.yaml`

**Examples:**
- hadolint Dockerfile -f sarif -o hadolint.sarif
- hadolint Dockerfile --verbose