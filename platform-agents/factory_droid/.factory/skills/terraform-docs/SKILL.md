---
name: "terraform-docs"
description: "Generates and maintains Terraform module documentation with terraform-docs: markdown tables, JSON, and CI enforcement of freshness. Use when working with docs generation, fmt and verify, devops or when the user mentions docs generation, fmt and verify, devops."
license: "MIT"
compatibility: "Requires terraform-docs."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "devops"}
allowed-tools: "Glob Grep Read Bash(terraform-docs:*)"
---

Generates and maintains Terraform module documentation with terraform-docs: markdown tables, JSON, and CI enforcement of freshness.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `terraform-docs markdown table .`, `terraform-docs fmt ./README.md`
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

# terraform-docs

Keep Terraform module documentation generated, consistent, and fresh.

## What This Skill Does

- Renders inputs/outputs/providers tables into README sections
- Supports markdown table, JSON, and Asciidoc formats
- Sorts sections and filters by required fields
- Fails CI when docs are stale (--check)
- Formats generated docs with terraform-docs fmt

## When to Use

- Publishing reusable modules with accurate usage docs
- CI gate ensuring README matches the code
- Onboarding docs for internal modules

## Real Commands

```bash
# Generate
terraform-docs markdown table .
terraform-docs markdown table --output-file README.md .
terraform-docs json . > docs.json
terraform-docs markdown . --sort-by-required
terraform-docs markdown table --show inputs,outputs .
terraform-docs markdown table --footer-from=./templates/footer.md .

# Format and verify
terraform-docs fmt ./README.md
terraform-docs markdown table --check .     # exit 1 when stale
terraform-docs version
```

## .terraform-docs.yml Example

```yaml
formatter: markdown table
output:
  file: README.md
  mode: inject
sort:
  enabled: true
settings:
  anchor: true
  hide-empty: true
```

## Best Practices

- Add `--check` to CI so docs cannot drift
- Use output mode inject to keep hand-written sections
- Commit generated docs (do not regenerate at apply time)
- Keep `examples/` directories in sync with README usage blocks
- Run terraform-docs after every module change, same commit

## Capabilities

### docs-generation
Generate README and JSON docs from Terraform code.

**Parameters:**
- `output-file` (string): File to write docs to
- `config` (string): Config file path

**Commands:**
- `terraform-docs markdown table .`
- `terraform-docs markdown table --output-file README.md .`
- `terraform-docs json . > docs.json`
- `terraform-docs markdown . --sort-by-required`
- `terraform-docs --config .terraform-docs.yml markdown table .`

**Examples:**
- terraform-docs markdown table --output-file README.md .
- terraform-docs json . > docs.json
- terraform-docs --config .terraform-docs.yml markdown table .

### fmt-and-verify
Format output and verify docs are up to date in CI.

**Parameters:**
- `check` (boolean): Fail if docs are stale
- `show` (string): Sections to show: inputs, outputs, providers, requirements

**Commands:**
- `terraform-docs fmt ./README.md`
- `terraform-docs markdown table --check .`
- `terraform-docs markdown table --footer-from=./templates/footer.md .`
- `terraform-docs markdown table --show inputs,outputs .`
- `terraform-docs version`

**Examples:**
- terraform-docs fmt ./README.md
- terraform-docs markdown table --check .
- terraform-docs markdown table --show inputs,outputs .

## References
- [terraform-docs Documentation](https://terraform-docs.io/)
- [terraform-docs GitHub](https://github.com/terraform-docs/terraform-docs)
