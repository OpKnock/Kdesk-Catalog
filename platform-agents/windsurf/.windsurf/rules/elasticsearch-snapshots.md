---
trigger: glob
description: "Elasticsearch snapshot and restore: register snapshot repositories, create and list snapshots, and restore indices from backups. Use when working with snapshot lifecycle, api or when the user mentions snapshot lifecycle, api."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

Elasticsearch snapshot and restore: register snapshot repositories, create and list snapshots, and restore indices from backups.

## Agentic Workflow: Read -> Reason -> Act (elasticsearch-snapshots)

You are **Elasticsearch Snapshots** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `elasticsearch-snapshots`
- Domain: Elasticsearch snapshot and restore: register snapshot repositories, create and list snapshots, and restore indices from backups.
- **snapshot-lifecycle**: Manage snapshot repositories, take snapshots, list them, and restore data. — `curl -s -X PUT 'localhost:9200/_snapshot/my_backup' -H 'Content-Type: applicatio`
- Check `knowledge` references before acting

### 2. Reason — think for `elasticsearch-snapshots`
- For `snapshot-lifecycle`: Manage snapshot repositories, take snapshots, list them, and restore data. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `elasticsearch-snapshots` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `elasticsearch-snapshots:5b72b683`

# Elasticsearch Snapshots

## What this skill does

Snapshots back up indices to a repository (S3, GCS, Azure, or shared filesystem) with incremental deduplication. Restore brings indices back with optional renaming. This skill covers the whole lifecycle.

## When to use

- Scheduled nightly backups of indices
- Restoring a corrupted index or migrating data between clusters
- Verifying backups are actually restorable

## Real commands

```bash
# Register an S3 repository (one-time per cluster)
curl -s -X PUT 'localhost:9200/_snapshot/my_backup' -H 'Content-Type: application/json' -d '{"type":"s3","settings":{"bucket":"es-backups","region":"us-east-1"}}' | jq

# Take a snapshot of specific indices
curl -s -X PUT 'localhost:9200/_snapshot/my_backup/snap_$(date +%Y%m%d)' -H 'Content-Type: application/json' -d '{"indices":"orders,users","ignore_unavailable":true}' | jq

# List snapshots and inspect status
curl -s 'localhost:9200/_snapshot/my_backup/_all?verbose=false' | jq '.snapshots[].snapshot'
curl -s 'localhost:9200/_snapshot/my_backup/snap_20240101/_status' | jq '.snapshots[0].stats.incremental'

# Restore with rename to avoid clobbering
curl -s -X POST 'localhost:9200/_snapshot/my_backup/snap_20240101/_restore' -H 'Content-Type: application/json' -d '{"indices":"orders","rename_pattern":"(.+)","rename_replacement":"restored_$1"}' | jq
```

## SLM policy example

```json
{
  "schedule": "0 30 2 * * ?",
  "name": "nightly-snap",
  "repository": "my_backup",
  "indices": ["orders", "users"],
  "retention": {"count": 14}
}
```

## Testing restores

```bash
# Monthly drill: restore into renamed index and delete after verification
curl -s -X POST 'localhost:9200/_snapshot/my_backup/snap_20240101/_restore' -H 'Content-Type: application/json' -d '{"indices":"orders","rename_pattern":"(.+)","rename_replacement":"restored_$1"}' | jq
curl -s 'localhost:9200/_cat/indices/restored_orders?v' | jq
```

## Best practices

- Never restore over a live index; always use rename_pattern.
- Enable `wait_for_completion=true` in scripts or poll _status.
- Retain at least 14 daily snapshots and run a restore drill monthly.
- Ensure the repo bucket has versioning for extra safety.

## Capabilities

### snapshot-lifecycle
Manage snapshot repositories, take snapshots, list them, and restore data.

**Parameters:**
- `repository` (string): Snapshot repository name
- `snapshot` (string): Snapshot name, e.g. snap_20240101
- `indices` (array): Indices to snapshot or restore

**Commands:**
- `curl -s -X PUT 'localhost:9200/_snapshot/my_backup' -H 'Content-Type: application/json' -d '{"type":"s3","settings":{"bucket":"es-backups","region":"us-east-1"}}' | jq`
- `curl -s -X PUT 'localhost:9200/_snapshot/my_backup/snap_$(date +%Y%m%d)' -H 'Content-Type: application/json' -d '{"indices":"orders,users","ignore_unavailable":true}' | jq`
- `curl -s 'localhost:9200/_snapshot/my_backup/_all?verbose=false' | jq '.snapshots[].snapshot'`
- `curl -s 'localhost:9200/_snapshot/my_backup/snap_20240101/_status' | jq '.snapshots[0].stats.incremental'`
- `curl -s -X POST 'localhost:9200/_snapshot/my_backup/snap_20240101/_restore' -H 'Content-Type: application/json' -d '{"indices":"orders","rename_pattern":"(.+)","rename_replacement":"restored_$1"}' | jq`

**Examples:**
- curl -s -X PUT 'localhost:9200/_snapshot/my_backup/snap_$(date +%Y%m%d)' -H 'Content-Type: application/json' -d '{"indices":"orders"}' | jq
- curl -s 'localhost:9200/_snapshot/my_backup/_all?verbose=false' | jq '.snapshots | length'
- curl -s -X POST 'localhost:9200/_snapshot/my_backup/snap_20240101/_restore' -H 'Content-Type: application/json' -d '{"indices":"orders"}' | jq

## References
- [Snapshot and Restore](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshot-restore.html)
- [S3 Repository Plugin](https://www.elastic.co/guide/en/elasticsearch/plugins/current/repository-s3.html)
