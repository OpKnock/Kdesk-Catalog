---
applyTo: "**/*.json **/*.r **/*.sh **/*.{yaml,yml}"
---

# popeye

Run full-cluster sanitizer scans and review reports. Customize scans with lint rules, ignore lists, and severity config. misconfigurations, and security issues.'

## Instructions

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
