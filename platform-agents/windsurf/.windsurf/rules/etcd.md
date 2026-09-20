---
trigger: glob
description: "Operates etcd key-value stores: read/write keys, watch changes, manage members, snapshots, backups, and cluster health. Use when working with kv operations, cluster and backup, devops or when the user mentions kv operations, cluster and backup, devops."
globs: ["**/*.r", "**/*.sh"]
---

Operates etcd key-value stores: read/write keys, watch changes, manage members, snapshots, backups, and cluster health.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `etcdctl put /config/app version 1.2.3`, `etcdctl member list`
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

# etcd Operations

Administer the etcd distributed key-value store backing Kubernetes and other systems.

## What This Skill Does

- Reads and writes keys with TTLs and prefixes
- Watches keys for change streams
- Manages cluster membership and health
- Takes and restores snapshots for DR
- Handles maintenance: defrag, compaction, alarms

## When to Use

- Debugging a control-plane outage (etcd quorum loss)
- Backing up Kubernetes cluster state
- Directly inspecting stored config or service discovery keys

## Real Commands

```bash
# Set env for TLS cluster
export ETCDCTL_API=3
export ETCDCTL_ENDPOINTS=https://10.0.0.1:2379,https://10.0.0.2:2379
export ETCDCTL_CACERT=/etc/kubernetes/pki/etcd/ca.crt
export ETCDCTL_CERT=/etc/kubernetes/pki/etcd/server.crt
export ETCDCTL_KEY=/etc/kubernetes/pki/etcd/server.key

# KV
etcdctl put /config/app version 1.2.3
etcdctl get /config/app --prefix
etcdctl del /temp --prefix
etcdctl watch /config/app

# Health and membership
etcdctl endpoint health --cluster
etcdctl endpoint status --cluster -w table
etcdctl member list -w table
etcdctl alarm list

# Backup / restore / defrag
etcdctl snapshot save /backups/etcd-$(date +%F).db
etcdctl snapshot restore /backups/etcd-2026-08-10.db --data-dir /var/lib/etcd-restore
etcdctl defrag --cluster
```

## Best Practices

- Always snapshot before upgrades: kubeadm/etcd version bumps
- Verify snapshots: `etcdctl snapshot status /backups/etcd-2026-08-10.db`
- Defrag periodically to reclaim space after compaction
- Keep 3 or 5 members; do not run even member counts
- Use `--prefix` carefully with `del` — double check the key space

## Capabilities

### kv-operations
Put, get, delete, and watch keys in the etcd database.

**Parameters:**
- `key` (string): Key path, e.g. /config/app
- `value` (string): Value to set
- `prefix` (boolean): Operate on key prefix

**Commands:**
- `etcdctl put /config/app version 1.2.3`
- `etcdctl get /config/app --prefix`
- `etcdctl get / --prefix --keys-only`
- `etcdctl del /temp/old --prefix`
- `etcdctl watch /config/app`
- `etcdctl get / --prefix --count-only`

**Examples:**
- etcdctl put /config/app version 1.2.3
- etcdctl get /config/app --prefix
- etcdctl watch /config/app

### cluster-and-backup
Manage members, check health, defrag, and take snapshots for backup.

**Parameters:**
- `endpoints` (string): Comma-separated etcd endpoints, e.g. 10.0.0.1:2379
- `snapshot-file` (string): Path to snapshot db file

**Commands:**
- `etcdctl member list`
- `etcdctl endpoint health --cluster`
- `etcdctl endpoint status --cluster -w table`
- `etcdctl snapshot save /backups/etcd-$(date +%F).db`
- `etcdctl snapshot restore /backups/etcd-2026-08-10.db --data-dir /var/lib/etcd-restore`
- `etcdctl defrag --cluster`

**Examples:**
- etcdctl endpoint health --cluster
- etcdctl snapshot save /backups/etcd-2026-08-10.db
- etcdctl member list -w table

## References
- [etcd Documentation](https://etcd.io/docs/)
- [etcdctl Manual](https://etcd.io/docs/latest/op-guide/maintenance/)
