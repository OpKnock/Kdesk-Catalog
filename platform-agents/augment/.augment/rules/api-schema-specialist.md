---
type: agent_requested
description: "Reviews and hardens API schemas with spectral: OpenAPI rulesets, custom rules, JSON output for CI, and schema quality gating. Use when working with spectral linting, schema review or when the user mentions spectral linting, schema review."
---

Reviews and hardens API schemas with spectral: OpenAPI rulesets, custom rules, JSON output for CI, and schema quality gating.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx @stoplight/spectral-cli lint openapi.yaml -r .spectral.y`, `npx @stoplight/spectral-cli lint openapi.yaml -r quality-rul`
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

# API Schema Specialist

Schema linting and review with spectral.

## What This Skill Does
- Lints OpenAPI contracts for consistency
- Enforces custom schema rules
- Exports reports for CI gating

## When to Use
- Reviewing schema PRs
- Enforcing API design standards
- Auditing legacy specs

## Real Commands

```bash
npx @stoplight/spectral-cli lint openapi.yaml -r .spectral.yml
npx @stoplight/spectral-cli lint openapi.yaml -f json -o report.json
npx @stoplight/spectral-cli lint openapi.yaml --fail-severity=warn
```

## Custom Rule

```yaml
rules:
  schemas-need-description:
    given: $.components.schemas[*]
    severity: error
    then:
      field: description
      function: truthy
```

## Testing
- Fail builds on error-severity violations
- Review JSON reports for triage
- Add rules incrementally

## Best Practices
- Extend a base ruleset before adding custom rules
- Document rule intent in comments
- Run lint in pre-merge checks

## Capabilities

### spectral-linting
Lint OpenAPI schemas with spectral

**Parameters:**
- `spec` (string): OpenAPI file to lint
- `ruleset` (string): Spectral ruleset path
- `format` (string): stylish, json, junit

**Commands:**
- `npx @stoplight/spectral-cli lint openapi.yaml -r .spectral.yml`
- `npx @stoplight/spectral-cli lint openapi.yaml -f json -o report.json`
- `npx @stoplight/spectral-cli lint openapi.yaml -f junit -o junit.xml`
- `npx @stoplight/spectral-cli lint openapi.yaml --fail-severity=warn`

**Examples:**
- -f json exports machine-readable results
- --fail-severity=warn makes warnings fail CI
- -f junit integrates with test reports

### schema-review
Enforce schema quality rules

**Commands:**
- `npx @stoplight/spectral-cli lint openapi.yaml -r quality-rules.yaml`
- `curl -s http://localhost:3000/openapi.json -o openapi.json`
- `npx @stoplight/spectral-cli lint openapi.json -r .spectral.yml`

**Examples:**
- -cli --help
- -api --help

## References
- [Spectral Docs](https://docs.stoplight.io/docs/spectral/)
- [Spectral CLI](https://github.com/stoplightio/spectral)