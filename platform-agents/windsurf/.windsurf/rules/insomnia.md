---
trigger: glob
description: "Design, test, and debug APIs with Insomnia: lint OpenAPI specs, run collections headlessly in CI, export design documents, and manage environments across stages. Use when working with inso cli, api or when the user mentions inso cli, api."
globs: ["**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

Design, test, and debug APIs with Insomnia: lint OpenAPI specs, run collections headlessly in CI, export design documents, and manage environments across stages.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `inso lint spec openapi.yaml`
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

# Insomnia

Design, test, and debug APIs with Insomnia and the inso CLI.

## What this skill does

- Lints OpenAPI specs with inso.
- Runs collections and assertion tests headlessly in CI.
- Exports design documents and generates configs.
- Manages environments for multi-stage testing.

## When to use

- Teams want API tests that run in CI without code.
- Validating OpenAPI specs before codegen.
- Replaying request suites after changes.

## Real commands

```bash
# Lint an OpenAPI spec
inso lint spec openapi.yaml

# Run collection tests against prod
inso run test "My Collection" --env prod

# Run requests only (no assertions)
inso run collection "My Collection" -e prod --verbose

# Export the spec as bundle
inso export spec openapi.yaml --output out/

# Generate an Insomnia config from a spec
inso generate config spec openapi.yaml
```

## CI usage

```bash
inso run test "Checkout" --env staging --reporter json --output results.json
# exit code reflects test failures
```

## Best practices

- Keep one environment per stage with secrets stored as variables.
- Write assertions in the Insomnia UI so the CLI run validates them.
- Run `inso lint spec` before every spec merge.
- Use --reporter json in CI for structured failure output.

## Example exchange

```
User: Run the Checkout tests against staging in CI.
Agent: inso run test "Checkout" --env staging --reporter json --output results.json
```

## Capabilities

### inso-cli
Lint API specs and run Insomnia collections and tests from CI.

**Parameters:**
- `spec_file` (string): OpenAPI spec path for lint/export.
- `collection` (string): Collection name to run.
- `env` (string): Environment (dev/staging/prod) for variables.

**Commands:**
- `inso lint spec openapi.yaml`
- `inso run test "My Collection" --env prod`
- `inso run collection "My Collection" -e prod --verbose`
- `inso export spec openapi.yaml --output out/`
- `inso generate config spec openapi.yaml`

**Examples:**
- inso lint spec openapi.yaml --ci
- inso run test "Checkout" -e staging --reporter json --output results.json
- inso run collection "Smoke" --env dev -t false

## References
- [Insomnia Docs](https://docs.insomnia.rest/)
- [Inso CLI Docs](https://docs.insomnia.rest/inso-cli/introduction)
