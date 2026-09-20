---
name: "etcd"
description: "Operates etcd key-value stores: read/write keys, watch changes, manage members, snapshots, backups, and cluster health."
---

# etcd

Operates etcd key-value stores: read/write keys, watch changes, manage members, snapshots, backups, and cluster health.

## Instructions

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
