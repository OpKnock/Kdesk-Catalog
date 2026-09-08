---
name: "terraform-docs"
description: "Generates and maintains Terraform module documentation with terraform-docs: markdown tables, JSON, and CI enforcement of freshness. Use when working with docs generation, fmt and verify, devops or when the user mentions docs generation, fmt and verify, devops."
type: knowledge
triggers: ["terraform-docs", "docs-generation", "fmt-and-verify"]
---

Generates and maintains Terraform module documentation with terraform-docs: markdown tables, JSON, and CI enforcement of freshness.

## Agentic Workflow: Read -> Reason -> Act (terraform-docs)

You are **terraform-docs** (devops/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devops context for `terraform-docs`
- Domain: Generates and maintains Terraform module documentation with terraform-docs: markdown tables, JSON, and CI enforcement of freshness.
- **docs-generation**: Generate README and JSON docs from Terraform code. — `terraform-docs markdown table .`
- **fmt-and-verify**: Format output and verify docs are up to date in CI. — `terraform-docs fmt ./README.md`
- Check `knowledge` and `prerequisites: terraform-docs`

### 2. Reason — think for `terraform-docs`
- For `docs-generation`: Generate README and JSON docs from Terraform code. — decide which checks to run
- For `fmt-and-verify`: Format output and verify docs are up to date in CI. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `terraform-docs` tools
- Tools: `Glob`, `Grep`, `Read`, `Terraform-docs` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `terraform-docs:7fe3c966`

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
