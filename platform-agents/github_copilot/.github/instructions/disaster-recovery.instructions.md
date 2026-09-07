---
applyTo: "**/*.r **/*.sh"
---

Implements Kubernetes disaster recovery with Velero: schedule backups, perform restores, migrate clusters, and verify RTO/RPO.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `velero install --provider aws --bucket velero-backups --secr`, `velero restore create --from-backup full-2026-08-10`
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

# Kubernetes Disaster Recovery

Protect clusters with Velero: versioned backups, scheduled snapshots, and verified restores.

## What This Skill Does

- Installs Velero with a provider plugin (AWS, Azure, GCP)
- Creates on-demand and scheduled backups (namespaces, PVs)
- Restores workloads to the same or a different cluster
- Migrates clusters with namespace remapping
- Validates backups with describe/logs

## When to Use

- Building a DR runbook for Kubernetes
- After an incident: restoring production workloads
- Cluster migration (old version -> new version, cloud -> cloud)

## Real Commands

```bash
# Install
velero install --provider aws --bucket velero-backups   --secret-file ./credentials-velero --plugins velero/velero-plugin-for-aws:v1.10.0

# Backups
velero backup create full-$(date +%F)
velero schedule create nightly --schedule='0 2 * * *' --include-namespaces app,db
velero backup get
velero backup describe full-2026-08-10 --details
velero backup logs full-2026-08-10

# Restores
velero restore create --from-backup full-2026-08-10
velero restore get
velero restore describe restore-20260810120000
velero restore logs restore-20260810120000

# Migration with namespace remap
velero restore create --from-backup full-2026-08-10   --namespace-mappings 'old-app:new-app'
```

## RTO/RPO Checklist

1. Schedule backups every 24h minimum (RPO)
2. Test a full restore quarterly and time it (RTO)
3. Store backups in a different region/account
4. Add `--include-cluster-resources=true` for full-fidelity restores
5. Enable volume snapshots for stateful workloads

## Best Practices

- Name backups with timestamps for retention policies
- Run restores into a staging cluster first, then production
- Use `velero backup logs` to find failed items after each backup
- Encrypt the backup bucket and restrict IAM to least privilege

## Capabilities

### velero-backups
Create on-demand and scheduled backups of cluster resources and persistent volumes.

**Parameters:**
- `schedule` (string): Cron expression for scheduled backups
- `include-namespaces` (string): Comma-separated namespaces to back up

**Commands:**
- `velero install --provider aws --bucket velero-backups --secret-file ./credentials-velero`
- `velero backup create full-$(date +%F) --include-namespaces app,db`
- `velero schedule create nightly --schedule='0 2 * * *' --include-namespaces app`
- `velero backup get`
- `velero backup describe full-2026-08-10`
- `velero backup logs full-2026-08-10`

**Examples:**
- velero backup create full-$(date +%F)
- velero schedule create nightly --schedule='0 2 * * *'
- velero backup describe full-2026-08-10 --details

### velero-restores
Restore clusters from backups and migrate between clusters.

**Parameters:**
- `from-backup` (string): Source backup name
- `namespace-mappings` (object): Map old namespace to new namespace

**Commands:**
- `velero restore create --from-backup full-2026-08-10`
- `velero restore get`
- `velero restore describe restore-20260810120000`
- `velero restore logs restore-20260810120000`
- `velero backup create restore --from-backup full-2026-08-10 --include-namespaces db`

**Examples:**
- velero restore create --from-backup full-2026-08-10
- velero restore describe restore-20260810120000
- velero restore logs restore-20260810120000

## References
- [Velero Documentation](https://velero.io/docs/)
- [Velero Plugins](https://velero.io/plugins/)
