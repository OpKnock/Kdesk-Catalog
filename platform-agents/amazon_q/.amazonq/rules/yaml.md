Parse, query, and transform structured documents with yq; validate syntax and style with yamllint; merge multi-document files; convert between markup formats, supporting API tooling workflows.

## Agentic Workflow: Read -> Reason -> Act (yaml)

You are **YAML** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `yaml`
- Domain: Parse, query, and transform structured documents with yq; validate syntax and style with yamllint; merge multi-document files; convert between markup formats, supporting API tooling workflows.
- **yaml-processing**: Query, validate, and transform YAML documents — `yq eval '.metadata.name' deployment.yaml`
- Check `knowledge` and `prerequisites: yamllint`

### 2. Reason — think for `yaml`
- For `yaml-processing`: Query, validate, and transform YAML documents — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `yaml` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Yamllint` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `yaml:6f00a5df`

# YAML

## What this skill does
Parse, query, and transform YAML files with yq; validate syntax and style with yamllint; merge multi-document files; and convert between YAML and JSON for API tooling.

## When to use
- Reading config from k8s manifests or CI files
- Transforming YAML in scripts/CI
- Validating hand-written YAML

## Real commands
```bash
# Query values
yq eval '.metadata.name' deployment.yaml
yq eval '.spec.containers[0].image' pod.yaml

# List keys
yq eval '.data | keys' configmap.yaml

# All images in a template
yq eval '.spec.template.spec.containers[].image' deployment.yaml | sort -u

# Merge base + overlay
yq eval-all 'select(di == 0) * select(di == 1)' base.yaml overlay.yaml

# Validate with yamllint (relaxed for k8s)
yamllint -d relaxed docker-compose.yml

# Convert YAML -> JSON
yq eval -o=json . config.yaml > config.json

# Convert JSON -> YAML
cat spec.json | yq eval -P - > spec.yaml
```

## Python fallback
```bash
python -c "import yaml,pprint;pprint.pprint(yaml.safe_load(open('config.yaml')))"
```

## Gotchas
- `yq` (mikefarah) vs `yq` (kislyuk): different syntax
- Use `-e` to exit non-zero when no matches
- Quote keys with special characters: `.\"app.kubernetes.io/name\"`

## Best practices
- Always lint YAML in CI before using it
- Avoid tabs; YAML forbids them in indentation
- Use `eastl` for alignment style consistency

## Testing
```bash
yamllint config.yaml && echo OK
yq eval '.spec.replicas' deployment.yaml
```

## Capabilities

### yaml-processing
Query, validate, and transform YAML documents

**Parameters:**
- `expression` (string): jq-style query expression
- `format` (string): Output format: yaml, json, xml, csv
- `file` (string): Input YAML file

**Commands:**
- `yq eval '.metadata.name' deployment.yaml`
- `yq eval '.spec.containers[0].image' pod.yaml`
- `yq eval-all 'select(di == 0) * select(di == 1)' base.yaml overlay.yaml`
- `yamllint -d relaxed docker-compose.yml`
- `yq eval -o=json . config.yaml > config.json`

**Examples:**
- yq eval '.data | keys' configmap.yaml
- yq eval '.spec.template.spec.containers[].image' deployment.yaml | sort -u
- python -c "import yaml;print(yaml.safe_load(open('config.yaml')))"

## References
- [yq on GitHub](https://github.com/mikefarah/yq)
- [YAML 1.2 Spec](https://yaml.org/spec/1.2.2/)