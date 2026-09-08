---
name: "kube-hunter"
description: "Probes Kubernetes clusters for exploitable attack surfaces with kube-hunter active and passive scans. Use when working with cluster hunting, reporting, security or when the user mentions cluster hunting, reporting, security."
---

Probes Kubernetes clusters for exploitable attack surfaces with kube-hunter active and passive scans.

## Agentic Workflow: Read -> Reason -> Act (kube-hunter)

You are **kube-hunter** (security/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — security context for `kube-hunter`
- Domain: Probes Kubernetes clusters for exploitable attack surfaces with kube-hunter active and passive scans.
- **cluster-hunting**: Scan clusters locally, remotely, or across CIDR ranges. — `kube-hunter`
- **reporting**: Capture findings to reports and logs. — `kube-hunter --report report.json --format json`
- Check `knowledge` and `prerequisites: kube-hunter`

### 2. Reason — think for `kube-hunter`
- For `cluster-hunting`: Scan clusters locally, remotely, or across CIDR ranges. — decide which checks to run
- For `reporting`: Capture findings to reports and logs. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `kube-hunter` tools
- Tools: `Glob`, `Grep`, `Read`, `Kube-hunter` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `kube-hunter:ff2a6a8a`

# kube-hunter

Penetration-test your Kubernetes cluster's attack surface.

## What This Skill Does

- Discovers clusters on local interfaces, remotes, or CIDRs
- Runs passive checks for known misconfigurations
- Runs active hunts for exposed API, dashboard, or RBAC issues
- Reports vulnerabilities with severity and remediation

## When to Use

- Pre-launch security assessment of a cluster
- Checking whether admin interfaces are exposed externally
- Recurring attack-surface audits

## Real Commands

```bash
# Discover from the local network
kube-hunter
kube-hunter --interface eth0

# Scan a remote API server
kube-hunter --remote k8s-api.example.com:6443

# Scan a subnet
kube-hunter --cidr 10.0.0.0/24

# Active hunting (tests exploits, use with care)
kube-hunter --active --remote 10.0.0.5:6443

# Reporting
kube-hunter --report report.html
kube-hunter --report findings.json --format json
```

## Best Practices

- Run active hunts only against test clusters or with authorization
- Pair with kube-bench (static CIS) for complementary coverage
- Re-run after networking or RBAC changes
- Treat findings as attack-surface candidates, not proof of compromise
- Automate passive scans weekly; active scans on release cadence

## Capabilities

### cluster-hunting
Scan clusters locally, remotely, or across CIDR ranges.

**Parameters:**
- `remote` (string): Remote endpoint host:port to scan
- `cidr` (string): CIDR range to scan for clusters
- `active` (boolean): Run active exploits/hunting checks

**Commands:**
- `kube-hunter`
- `kube-hunter --remote 10.0.0.5:6443`
- `kube-hunter --cidr 10.0.0.0/24`
- `kube-hunter --active`
- `kube-hunter --interface eth0`

**Examples:**
- kube-hunter --remote k8s-api.example.com:6443
- kube-hunter --cidr 192.168.1.0/24
- kube-hunter --active --remote 10.0.0.5:6443

### reporting
Capture findings to reports and logs.

**Parameters:**
- `report` (string): Report file path
- `format` (string): Report format: html, json, console

**Commands:**
- `kube-hunter --report report.json --format json`
- `kube-hunter --report report.html --format html`
- `kube-hunter --log /tmp/kube-hunter.log`
- `kube-hunter --active --report report.html`

**Examples:**
- kube-hunter --report report.html
- kube-hunter --report findings.json --format json
- kube-hunter --active --report report.html

## References
- [kube-hunter GitHub](https://github.com/aquasecurity/kube-hunter)
- [kube-hunter Hunting Scenarios](https://github.com/aquasecurity/kube-hunter/blob/master/docs/HUNTING_SCENARIOS.md)
