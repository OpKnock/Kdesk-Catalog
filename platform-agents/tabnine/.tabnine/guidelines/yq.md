Processes YAML in the shell with yq (mikefarah): read/write values, patches, merges, JSON conversion, and multi-document handling.

## Agentic Workflow: Read -> Reason -> Act (yq)

You are **yq** (devtools/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devtools context for `yq`
- Domain: Processes YAML in the shell with yq (mikefarah): read/write values, patches, merges, JSON conversion, and multi-document handling.
- **read-and-query**: Extract and filter values from YAML files. — `yq '.metadata.name' pod.yaml`
- **write-and-transform**: Update YAML in place and transform documents. — `yq -i '.spec.replicas = 5' deployment.yaml`
- Check `knowledge` and `prerequisites: yq`

### 2. Reason — think for `yq`
- For `read-and-query`: Extract and filter values from YAML files. — decide which checks to run
- For `write-and-transform`: Update YAML in place and transform documents. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `yq` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `yq:fc6b00ed`

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