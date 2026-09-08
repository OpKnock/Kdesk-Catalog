Audits and enforces API governance on existing OpenAPI specs, blocking non-compliant changes via CI linting with Spectral rulesets.

## Agentic Workflow: Read -> Reason -> Act (api-gov-governance-audit)

You are **Api Gov Governance Audit** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `api-gov-governance-audit`
- Domain: Audits and enforces API governance on existing OpenAPI specs, blocking non-compliant changes via CI linting with Spectral rulesets.
- **governance-audit**: Run Spectral linting against existing OpenAPI specs to surface style guide violations and drift — `npx @stoplight/spectral-cli lint openapi.yaml`
- **compliance-gates**: Wire lint gates into CI/CD so non-compliant API changes fail the pipeline — `npx @stoplight/spectral-cli lint --fail-severity warn openapi.yaml`
- Check `knowledge` and `prerequisites: spectral, openapi`

### 2. Reason — think for `api-gov-governance-audit`
- For `governance-audit`: Run Spectral linting against existing OpenAPI specs to surface style guide violations and drift — decide which checks to run
- For `compliance-gates`: Wire lint gates into CI/CD so non-compliant API changes fail the pipeline — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-gov-governance-audit` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx`, `Redocly` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-gov-governance-audit:0fcc50d6`

# API Gov (Audit & Enforce)

Audits existing OpenAPI specs against an organizational style guide and enforces compliance in CI.

## When to Use
- Enforcing standards on a mature spec base
- Blocking breaking or non-compliant PRs
- Measuring governance drift over time
- Onboarding teams onto a published style guide

## Real Commands

```bash
# Install tooling
npm install -g @stoplight/spectral-cli
npm install -g @redocly/cli

# Lint a spec
npx @stoplight/spectral-cli lint openapi.yaml

# Lint with a custom ruleset
npx @stoplight/spectral-cli lint --ruleset .spectral.yaml --format json openapi.yaml

# Recommended defaults
redocly lint openapi.yaml --extends=recommended

# Validate structure first
swagger-cli validate openapi.yaml
```

## CI Gate

```yaml
# .github/workflows/api-governance.yml
- name: Lint specs
  run: npx @stoplight/spectral-cli lint --fail-severity error ${{ matrix.spec }}
```

## Testing
Run the linter on the PR branch against the main branch baseline and compare JSON reports.

## Best Practices
- Publish the style guide alongside the ruleset
- Use `--fail-severity error` in CI, `warn` locally
- Review lint report trends each sprint

## Capabilities

### governance-audit
Run Spectral linting against existing OpenAPI specs to surface style guide violations and drift

**Parameters:**
- `spec` (string): Path to the OpenAPI spec to lint
- `ruleset` (string): Path to the Spectral ruleset file
- `format` (string): Output format: stylish, json, github-actions

**Commands:**
- `npx @stoplight/spectral-cli lint openapi.yaml`
- `npx @stoplight/spectral-cli lint --ruleset .spectral.yaml --format json openapi.yaml`
- `redocly lint openapi.yaml --extends=recommended`
- `swagger-cli validate openapi.yaml`
- `npx @stoplight/spectral-cli lint --fail-severity error openapi.yaml`

**Examples:**
- npx @stoplight/spectral-cli lint --ruleset .spectral.yaml --format json openapi.yaml > spectral-report.json
- redocly lint api/v1/*.yaml --output-style=github-actions
- swagger-cli validate openapi.yaml && npx @stoplight/spectral-cli lint openapi.yaml

### compliance-gates
Wire lint gates into CI/CD so non-compliant API changes fail the pipeline

**Parameters:**
- `baseRef` (string): Git ref to diff spec changes against
- `failSeverity` (string): Minimum severity that fails CI

**Commands:**
- `npx @stoplight/spectral-cli lint --fail-severity warn openapi.yaml`
- `npx @stoplight/spectral-cli lint --fail-on-unmatched-globs openapi.yaml`
- `git diff --name-only HEAD~1 | grep -E '\.(yaml|yml|json)$' | xargs npx @stoplight/spectral-cli lint`
- `openapi-diff --fail-on-incompatible old.yaml new.yaml`
- `npx @stoplight/spectral-cli lint --summary openapi.yaml`

**Examples:**
- git diff --name-only HEAD~1 | xargs npx @stoplight/spectral-cli lint --fail-severity error
- openapi-diff --fail-on-incompatible prod-spec.yaml pr-spec.yaml
- npx @stoplight/spectral-cli lint --summary --quiet openapi.yaml

## References
- [Spectral Documentation](https://docs.stoplight.io/docs/spectral)
- [OpenAPI Specification 3.1](https://spec.openapis.org/oas/v3.1.0)
- [Redocly CLI](https://redocly.com/docs/cli/)