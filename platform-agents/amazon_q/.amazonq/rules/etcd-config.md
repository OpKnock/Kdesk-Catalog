etcd cluster configuration and operations: read and write keys, inspect member health, and manage leases and snapshots.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `etcdctl put /config/database/url postgres://db:5432/app --en`
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

# etcd Config

## What this skill does

etcd is a distributed key-value store used for service discovery and shared config. This skill covers reading/writing keys, checking member health, managing leases, and taking snapshots.

## When to use

- Debugging why a service reads stale config
- Checking cluster quorum after member changes
- Taking a backup before an upgrade

## Real commands

```bash
# Write and read config keys
etcdctl put /config/database/url postgres://db:5432/app --endpoints=https://etcd-1:2379
etcdctl get /config --prefix --keys-only

# Health and status
etcdctl endpoint health --endpoints=https://etcd-1:2379,https://etcd-2:2379
etcdctl endpoint status --write-out=table --endpoints=https://etcd-1:2379

# Members and leadership
etcdctl member list --write-out=table

# Backup and lease
etcdctl snapshot save backup.db
etcdctl snapshot status backup.db
etcdctl lease grant 300
```

## Cluster size guidance

- Odd member counts: 3 or 5.
- 3 members tolerate 1 failure; 5 tolerate 2.
- Never run 2 members; split-brain risk.

## Maintenance commands

```bash
# Check alarms (e.g. NOSPACE)
etcdctl alarm list
# Defragment a member
etcdctl defrag --endpoints=https://etcd-1:2379
```

## Best practices

- Always use TLS for production endpoints; verify with --cacert.
- Snapshot before any etcd upgrade and test restore on staging.
- Keep keys small; etcd is not a blob store.
- Use leases for ephemeral registration keys (service discovery).
- Add `--command-timeout` in scripts so hangs don't block deploys.

## Capabilities

### etcd-ops
Manage keys, leases, members, and snapshots of an etcd cluster with etcdctl.

**Parameters:**
- `endpoints` (array): Comma-separated etcd endpoints
- `key` (string): Key path to read or write
- `prefix` (string): Prefix for range operations

**Commands:**
- `etcdctl put /config/database/url postgres://db:5432/app --endpoints=https://etcd-1:2379`
- `etcdctl get /config --prefix --keys-only`
- `etcdctl endpoint health --endpoints=https://etcd-1:2379,https://etcd-2:2379`
- `etcdctl endpoint status --write-out=table --endpoints=https://etcd-1:2379`
- `etcdctl member list --write-out=table`
- `etcdctl snapshot save backup.db`
- `etcdctl lease grant 300`

**Examples:**
- etcdctl get /config --prefix --keys-only
- etcdctl endpoint health --endpoints=https://etcd-1:2379,https://etcd-2:2379
- etcdctl snapshot save backup.db && etcdctl snapshot status backup.db

## References
- [etcdctl documentation](https://etcd.io/docs/v3.5/dev-guide/interacting_v3/)
- [etcd Operations Guide](https://etcd.io/docs/v3.5/op-guide/maintenance/)