---
applyTo: "**/*.go **/*.json **/*.r **/*.scala **/*.sh **/*.{yaml,yml}"
---

Implements automated API governance: Spectral rulesets, PR review bots, and CI gates for OpenAPI quality.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx @stoplight/spectral-cli lint --ruleset .spectral.yaml op`, `mkdir -p .github/workflows`
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

# API Governance Engineer

Implements governance tooling: lint rules, CI gates, and PR checks.

## When to Use
- Enforcing API conventions mechanically
- Blocking non-compliant PRs
- Standardizing review effort

## Real Commands

```bash
# Local lint
npx @stoplight/spectral-cli lint --ruleset .spectral.yaml openapi.yaml

# JSON report
npx @stoplight/spectral-cli lint --ruleset .spectral.yaml --format json openapi.yaml > report.json

# CI-friendly annotations
npx @stoplight/spectral-cli lint --ruleset .spectral.yaml --format github-actions openapi.yaml

# Diff-based checks
npx @stoplight/spectral-cli lint --ruleset .spectral.yaml --fail-severity error openapi.yaml
```

## Ruleset Structure

```yaml
extends: [[spectral:oas, recommended]]
rules:
  path-kebab-case:
    message: Paths must use kebab-case
    given: $.paths[*]~
    then: {function: pattern, functionOptions: {match: '^/.*[a-z0-9-]*$'}}
```

## Testing
Create a violating spec fixture and assert the gate fails, then assert it passes after fixes.

## Best Practices
- Start warn, escalate to error over time
- Keep the ruleset in version control

## Capabilities

### ci-linting
Run Spectral in CI with custom rulesets and JSON reports

**Parameters:**
- `ruleset` (string): Spectral ruleset path
- `spec` (string): OpenAPI spec path

**Commands:**
- `npx @stoplight/spectral-cli lint --ruleset .spectral.yaml openapi.yaml`
- `npx @stoplight/spectral-cli lint --ruleset .spectral.yaml --format json openapi.yaml > report.json`
- `npx @stoplight/spectral-cli lint --ruleset .spectral.yaml --fail-severity error openapi.yaml`
- `npx @stoplight/spectral-cli lint --ruleset .spectral.yaml --verbose openapi.yaml`
- `node -e "const r=require('./report.json');console.log(r.filter(x=>x.severity===0).length+' errors')"`

**Examples:**
- npx @stoplight/spectral-cli lint --ruleset .spectral.yaml --fail-severity error openapi.yaml
- npx @stoplight/spectral-cli lint --ruleset .spectral.yaml --format json openapi.yaml > report.json && node -e "const r=require('./report.json');console.log(r.length+' violations')"
- npx @stoplight/spectral-cli lint --ruleset .spectral.yaml --verbose openapi.yaml

### pr-checks
Wire governance checks into pull requests with GitHub Actions

**Parameters:**
- `baseRef` (string): Base branch for diffs
- `workflow` (string): Workflow file path

**Commands:**
- `mkdir -p .github/workflows`
- `node -e "const fs=require('fs');fs.writeFileSync('.github/workflows/api-lint.yml','name: api-lint\non: [pull_request]\njobs:\n  lint:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - run: npx @stoplight/spectral-cli lint -r .spectral.yaml openapi.yaml\n')"`
- `git add .github/workflows/api-lint.yml && git commit -m 'add API lint gate'`
- `npx @stoplight/spectral-cli lint --ruleset .spectral.yaml --format github-actions openapi.yaml`
- `git diff --name-only origin/main HEAD | grep openapi | xargs npx @stoplight/spectral-cli lint`

**Examples:**
- npx @stoplight/spectral-cli lint --ruleset .spectral.yaml --format github-actions openapi.yaml
- git diff --name-only origin/main HEAD | grep openapi | xargs npx @stoplight/spectral-cli lint
- git add .github/workflows/api-lint.yml && git commit -m 'add API lint gate'

## References
- [Spectral CLI Reference](https://docs.stoplight.io/docs/spectral/reference/cli)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
