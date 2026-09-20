---
name: "hadolint"
description: "Lints Dockerfiles with hadolint: best-practice rules, shellcheck integration, and CI enforcement. Use when working with hadolint lint, hadolint config, code quality or when the user mentions hadolint lint, hadolint config, code quality."
---

Lints Dockerfiles with hadolint: best-practice rules, shellcheck integration, and CI enforcement.

## Agentic Workflow: Read -> Reason -> Act (hadolint)

You are **hadolint** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `hadolint`
- Domain: Lints Dockerfiles with hadolint: best-practice rules, shellcheck integration, and CI enforcement.
- **hadolint-lint**: Lint Dockerfiles from CLI or stdin. — `hadolint Dockerfile`
- **hadolint-config**: Manage rules and formats. — `hadolint --version`
- Check `knowledge` and `prerequisites: docker, hadolint`

### 2. Reason — think for `hadolint`
- For `hadolint-lint`: Lint Dockerfiles from CLI or stdin. — decide which checks to run
- For `hadolint-config`: Manage rules and formats. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `hadolint` tools
- Tools: `Glob`, `Grep`, `Read`, `Hadolint`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `hadolint:816d4709`

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

**Parameters:**
- `file` (string): Dockerfile path
- `ignore` (string): Rules to ignore
- `failure-threshold` (string): error, warning, info, style

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

**Parameters:**
- `format` (string): tty, json, sarif, checkstyle
- `output` (string): Report output file path

**Commands:**
- `hadolint --version`
- `hadolint Dockerfile --format sarif`
- `hadolint Dockerfile --no-color`
- `hadolint Dockerfile --config .hadolint.yaml`

**Examples:**
- hadolint Dockerfile -f sarif -o hadolint.sarif
- hadolint Dockerfile --verbose

## References
- [Hadolint Docs](https://github.com/hadolint/hadolint)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
