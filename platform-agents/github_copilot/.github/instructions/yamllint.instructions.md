---
applyTo: "**/*.json **/*.r **/*.sh **/*.{yaml,yml}"
---

Validate YAML style and syntax with configurable rules.

## Agentic Workflow: Read -> Reason -> Act (yamllint)

You are **yamllint** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `yamllint`
- Domain: Validate YAML style and syntax with configurable rules.
- **yamllint**: Validate YAML style and syntax with configurable rules — `yamllint config.yaml`
- Check `knowledge` and `prerequisites: yamllint`

### 2. Reason — think for `yamllint`
- For `yamllint`: Validate YAML style and syntax with configurable rules — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `yamllint` tools
- Tools: `Glob`, `Grep`, `Read`, `Yamllint` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `yamllint:04b7d271`

# yamllint

Linter for YAML: catches syntax errors, inconsistent indentation, and style
violations in configs, CI pipelines, and manifests.

## When to Use

- Validating CI pipeline YAML before push
- Enforcing consistent YAML style across a repo
- Checking Kubernetes manifests and compose files

## Real Commands

```bash
# Install
pip install yamllint

# Check a file
sudo yamllint docker-compose.yml

# Check a directory with a config
sudo yamllint -c .yamllint .

# Strict: warnings also fail
sudo yamllint --strict .github/workflows/

# JSON for CI
sudo yamllint --format json . > yamllint-report.json

# One-off inline config
sudo yamllint -d "{extends: default, rules: {line-length: {max: 120}}}" k8s/

# Ignore generated files
sudo yamllint --ignore '*.lock' .
```

## Config (.yamllint)

```yaml
---
extends: default
rules:
  line-length:
    max: 120
  document-start: disable
  truthy: disable
```

## CI

```yaml
- name: YAML lint
  run: yamllint -c .yamllint .
```

## Best Practices

- Commit `.yamllint` so all CI runs agree
- Disable rules project-wide instead of adding `# yamllint disable-line` everywhere
- Run before `kubectl apply` to catch indentation bugs in manifests
- Use `--strict` only on curated YAML; otherwise it fails on style nits

## Example Response

Returns `file:line:col: level message (rule)` per violation and exits non-zero
on errors (or warnings with --strict).

## Capabilities

### yamllint
Validate YAML style and syntax with configurable rules

**Parameters:**
- `config` (string): Path to the yamllint config file
- `format` (string): Output format: standard, github, colored, parsable, json
- `strict` (boolean): Return non-zero if any warning (not just errors) is found

**Commands:**
- `yamllint config.yaml`
- `yamllint -c .yamllint src/`
- `yamllint --strict pipeline.yml`
- `yamllint --format json .`
- `yamllint -d "{extends: default, rules: {line-length: disable}}" deploy.yml`

**Examples:**
- yamllint --ignore "*.generated.yaml" .
- yamllint --format github .
- yamllint --no-warnings k8s/

## References
- [yamllint docs](https://yamllint.readthedocs.io/)
- [yamllint configuration](https://yamllint.readthedocs.io/en/stable/configuration.html)
