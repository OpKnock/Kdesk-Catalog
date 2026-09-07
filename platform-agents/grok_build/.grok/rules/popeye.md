Run full-cluster sanitizer scans and review reports. Customize scans with lint rules, ignore lists, and severity config. misconfigurations, and security issues.'

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `popeye`, `popeye --lint < rules.yaml`
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

# Popeye Cluster Sanitizer

Audit Kubernetes clusters for hygiene violations: missing probes, resource limits, deprecated APIs, and security smells.

## What This Skill Does

- Scans live cluster resources against best-practice lint rules
- Reports severity-ranked violations (ok, info, warning, error)
- Scopes scans by namespace or label selector
- Saves JSON/YAML reports for CI and dashboards
- Supports custom rule overrides

## When to Use

- Pre-release cluster audit
- Spotting risky patterns (no probes, no limits, root containers)
- CI gate on cluster hygiene

## Real Commands

```bash
# Full scan
popeye
popeye -A
popeye -n kube-system
popeye --context prod

# Reports
popeye --save                 # writes report to file
popeye -o yaml
popeye -n app -o json > report.json
popeye -o junit > report.xml

# Customization
popeye --lint < rules.yaml
popeye --overrides overrides.yaml
popeye -l app=web
popeye --clear-cache
```

## What It Checks

- Resource limits/requests missing
- Readiness/liveness probes absent
- Containers running as root
- Deprecated apiVersions
- Excess replicas of ReplicaSets
- Secrets mounted as env vs files

## Best Practices

- Run popeye weekly and after every major release
- Feed JSON output into dashboards for trend tracking
- Combine with pluto for deprecation scanning and trivy for images
- Use --overrides to codify your team's exceptions explicitly
- Gate on ERROR severity only initially; ratchet down over time

## Capabilities

### cluster-sanitize
Run full-cluster sanitizer scans and review reports.

**Parameters:**
- `namespace` (string): Namespace scope
- `output` (string): Report format: standard, json, yaml, junit
- `save` (boolean): Write report to file

**Commands:**
- `popeye`
- `popeye -n kube-system`
- `popeye -A`
- `popeye --save`
- `popeye -o yaml`
- `popeye --context prod`

**Examples:**
- popeye
- popeye -n kube-system
- popeye --save

### rules-and-overrides
Customize scans with lint rules, ignore lists, and severity config.

**Parameters:**
- `lint` (string): Inline YAML lint rules via stdin
- `overrides` (string): Overrides file

**Commands:**
- `popeye --lint < rules.yaml`
- `popeye --overrides overrides.yaml`
- `popeye -l app=web`
- `popeye --clear-cache`
- `popeye -n app -o json > report.json`

**Examples:**
- popeye --lint < rules.yaml
- popeye --overrides overrides.yaml
- popeye -n app -o json > report.json

## References
- [Popeye GitHub](https://github.com/derailed/popeye)
- [Popeye Config Reference](https://github.com/derailed/popeye/blob/master/README.md#configuration)