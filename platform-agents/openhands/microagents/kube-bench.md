---
name: "kube-bench"
description: "Runs CIS Kubernetes Benchmark checks against master, worker, etcd, and control-plane components with the kube-bench auditor. Use when working with benchmark runs, reporting, security or when the user mentions benchmark runs, reporting, security."
type: knowledge
triggers: ["kube-bench", "benchmark-runs", "reporting"]
---

Runs CIS Kubernetes Benchmark checks against master, worker, etcd, and control-plane components with the kube-bench auditor.

## Agentic Workflow: Read -> Reason -> Act (kube-bench)

You are **kube-bench** (security/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — security context for `kube-bench`
- Domain: Runs CIS Kubernetes Benchmark checks against master, worker, etcd, and control-plane components with the kube-bench auditor.
- **benchmark-runs**: Run CIS checks against node roles and Kubernetes versions. — `kube-bench`
- **reporting**: Produce JSON and JUnit reports for compliance evidence. — `kube-bench run --json`
- Check `knowledge` and `prerequisites: kube-bench`

### 2. Reason — think for `kube-bench`
- For `benchmark-runs`: Run CIS checks against node roles and Kubernetes versions. — decide which checks to run
- For `reporting`: Produce JSON and JUnit reports for compliance evidence. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `kube-bench` tools
- Tools: `Glob`, `Grep`, `Read`, `Kube-bench` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `kube-bench:c6f495a1`

# kube-bench

Audit Kubernetes clusters against the CIS Kubernetes Benchmark.

## What This Skill Does

- Runs CIS checks against master, worker, and etcd components
- Matches benchmark checks to the cluster's Kubernetes version
- Outputs JSON/JUnit reports for compliance and CI
- Identifies the exact control-plane flags to harden

## When to Use

- Pre-deployment security audit of a cluster
- Compliance evidence for CIS or SOC2 controls
- Periodic hardening reviews of node configuration

## Real Commands

```bash
# Run against all node roles
kube-bench

# Scope by role
kube-bench run --targets master
kube-bench run --targets worker
kube-bench run --targets etcd

# Version-specific benchmark
kube-bench run --version 1.28

# Targeted checks and reporting
kube-bench run --check 1.2.7,1.4.1
kube-bench run --json --outputfile report.json
kube-bench run --junit --junitfile junit.xml
```

## In-Cluster Run

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: kube-bench
spec:
  template:
    spec:
      hostPID: true
      containers:
        - name: kube-bench
          image: aquasec/kube-bench:latest
          command: ["/bin/sh", "-c", "kube-bench run --json --outputfile /reports/report.json"]
      restartPolicy: Never
```

## Best Practices

- Run per node role and store JSON artifacts per node
- Re-run after every Kubernetes upgrade; checks change with versions
- Automate remediation for repeated failures (e.g. flag-level config)
- Pair with kube-hunter or kubescape for active and posture testing
- Track failures as tracked exemptions, not silence

## Capabilities

### benchmark-runs
Run CIS checks against node roles and Kubernetes versions.

**Parameters:**
- `targets` (string): Comma-separated node roles: master, worker, etcd, policypki
- `version` (string): Kubernetes version for the benchmark
- `check` (string): Specific check IDs to run, e.g. 1.2.7,1.4.1

**Commands:**
- `kube-bench`
- `kube-bench run --targets master`
- `kube-bench run --targets etcd`
- `kube-bench run --version 1.28`
- `kube-bench run --check 1.2.7,1.4.1`

**Examples:**
- kube-bench run --targets master,worker
- kube-bench run --version 1.28 --targets etcd
- kube-bench --json

### reporting
Produce JSON and JUnit reports for compliance evidence.

**Parameters:**
- `outputfile` (string): File path for JSON results
- `junitfile` (string): File path for JUnit XML results

**Commands:**
- `kube-bench run --json`
- `kube-bench run --json --outputfile kube-bench-report.json`
- `kube-bench run --junit --junitfile junit.xml`
- `kube-bench install`
- `kube-bench run --verbose`

**Examples:**
- kube-bench run --json --outputfile report.json
- kube-bench run --junit --junitfile junit.xml
- kube-bench install && kube-bench

## References
- [kube-bench GitHub](https://github.com/aquasecurity/kube-bench)
- [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes)
