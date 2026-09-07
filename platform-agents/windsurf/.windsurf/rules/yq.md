---
trigger: glob
description: "Processes YAML in the shell with yq (mikefarah): read/write values, patches, merges, JSON conversion, and multi-document handling. Use when working with read and query, write and transform, devtools or when the user mentions read and query, write and transform, devtools."
globs: ["**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

Processes YAML in the shell with yq (mikefarah): read/write values, patches, merges, JSON conversion, and multi-document handling.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `yq '.metadata.name' pod.yaml`, `yq -i '.spec.replicas = 5' deployment.yaml`
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

# yq YAML Processing

Query and edit YAML files like jq does for JSON.

## What This Skill Does

- Reads values with jq-like expressions
- Edits YAML in place (-i)
- Converts between YAML and JSON
- Merges multi-document files
- Transforms with operators (|=, del, load)

## When to Use

- Patching Kubernetes manifests in scripts
- Reading values from config files in CI
- Converting YAML configs to JSON for APIs

## Real Commands

```bash
# Read
yq '.metadata.name' pod.yaml
yq '.spec.containers[0].image' pod.yaml
yq '.items[] | select(.kind == "Deployment")' all.yaml
yq '. | length' services.yaml

# Write
yq -i '.spec.replicas = 5' deployment.yaml
yq -i '.spec.template.spec.containers[0].image = "nginx:1.27"' deployment.yaml
yq -i '.metadata.labels.owner = "platform"' config.yaml
yq -i 'del(.spec.tolerations)' deployment.yaml

# Transform
yq '.spec.replicas |= . * 2' deployment.yaml
yq -o=json . config.yaml
yq eval-all '. as $item ireduce ({}; . * $item)' a.yaml b.yaml
yq -i '.data = load("values.json")' config.yaml
```

## Best Practices

- Use -i only on files in version control
- Back up manifests before batch edits
- Use eval-all for multi-document merges
- Validate output: yq ... | kubectl apply --dry-run=client -f -
- Prefer yq over sed/awk for structured YAML changes

## Capabilities

### read-and-query
Extract and filter values from YAML files.

**Parameters:**
- `expression` (string): yq expression
- `file` (string): YAML file path

**Commands:**
- `yq '.metadata.name' pod.yaml`
- `yq '.spec.containers[0].image' pod.yaml`
- `yq '.items[] | select(.kind == "Deployment")' all.yaml`
- `yq '. | length' services.yaml`
- `yq eval-all '. as $item ireduce ({}; . * $item)' a.yaml b.yaml`
- `yq -o=json . config.yaml`

**Examples:**
- yq '.spec.containers[0].image' pod.yaml
- yq '.items[] | select(.kind == "Deployment")' all.yaml
- yq -o=json . config.yaml

### write-and-transform
Update YAML in place and transform documents.

**Parameters:**
- `in-place` (boolean): Edit file in place (-i)
- `path` (string): YAML path expression

**Commands:**
- `yq -i '.spec.replicas = 5' deployment.yaml`
- `yq -i '.spec.template.spec.containers[0].image = "nginx:1.27"' deployment.yaml`
- `yq -i '.metadata.labels.owner = "platform"' config.yaml`
- `yq '.spec.replicas |= . * 2' deployment.yaml`
- `yq -i 'del(.spec.tolerations)' deployment.yaml`
- `yq -i '.data = load("values.json")' config.yaml`

**Examples:**
- yq -i '.spec.replicas = 5' deployment.yaml
- yq -i '.metadata.labels.owner = "platform"' config.yaml
- yq -i 'del(.spec.tolerations)' deployment.yaml

## References
- [yq (mikefarah) Docs](https://mikefarah.gitbook.io/yq)
- [yq GitHub](https://github.com/mikefarah/yq)
