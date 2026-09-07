---
name: "hadolint"
description: "Lints Dockerfiles with hadolint: best-practice rules, shellcheck integration, and CI enforcement. Use when working with hadolint lint, hadolint config, code quality or when the user mentions hadolint lint, hadolint config, code quality."
license: "MIT"
compatibility: "Requires docker, hadolint."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "code-quality"}
allowed-tools: "Glob Grep Read Bash(docker:*) Bash(hadolint:*)"
---

Lints Dockerfiles with hadolint: best-practice rules, shellcheck integration, and CI enforcement.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `hadolint Dockerfile`, `hadolint --version`
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
