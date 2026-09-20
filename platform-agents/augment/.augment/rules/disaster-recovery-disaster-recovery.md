---
type: agent_requested
description: "Plans and executes disaster recovery for databases and files: RTO/RPO design, pg_dump/restic/rclone backups, and restore drills. Use when working with database backup, file and object backup or when the user mentions database backup, file and object backup."
---

Plans and executes disaster recovery for databases and files: RTO/RPO design, pg_dump/restic/rclone backups, and restore drills.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `pg_dump -Fc -d mydb -f mydb.dump`, `restic init --repo s3:s3.amazonaws.com/bucket/restic`
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

# Disaster Recovery Planning

Protect systems with real backup tooling and measurable restore targets.

## What This Skill Does

- Backs up and restores databases (Postgres, MySQL, MongoDB)
- Takes encrypted incremental file backups with restic
- Syncs objects to cloud storage with rclone/aws s3
- Defines RTO/RPO per workload tier
- Runs restore drills to verify recoverability

## When to Use

- Designing a DR plan for an application
- Recovering after data loss or corruption
- Auditing whether backups actually restore

## Real Commands

```bash
# PostgreSQL
pg_dump -Fc -d mydb -f mydb.dump
pg_restore -d newdb mydb.dump
pg_dumpall -f cluster.sql

# MySQL / MongoDB
mysqldump -u root mydb > mydb.sql
mysql -u root mydb < mydb.sql
mongodump --db mydb --out /backups/mongo
mongorestore --db mydb /backups/mongo/mydb

# Files (restic, encrypted)
restic init --repo s3:s3.amazonaws.com/bucket/restic
restic backup --repo r: /srv/data
restic snapshots --repo r:
restic restore latest --repo r: --target /restore
restic forget --repo r: --keep-daily 14 --prune

# Cloud sync
rclone copy /srv/data remote:backups --checksum
aws s3 sync /srv/data s3://bucket/backups --delete
```

## Tiering by RPO/RTO

- Tier 1 (minutes): replication + WAL streaming
- Tier 2 (hours): nightly dumps + restic snapshots
- Tier 3 (days): weekly object sync

## Best Practices

- Test restores quarterly; untested backups are wishes
- Encrypt backups (restic default, KMS for S3)
- Store offsite: different region, immutable buckets
- Automate drills and record restore times
- Document runbooks per tier with exact commands

## Capabilities

### database-backup
Back up and restore PostgreSQL, MySQL, and MongoDB.

**Parameters:**
- `database` (string): Database name
- `out` (string): Backup output path

**Commands:**
- `pg_dump -Fc -d mydb -f mydb.dump`
- `pg_restore -d newdb mydb.dump`
- `mysqldump -u root mydb > mydb.sql`
- `mysql -u root mydb < mydb.sql`
- `mongodump --db mydb --out /backups/mongo`
- `mongorestore --db mydb /backups/mongo/mydb`

**Examples:**
- pg_dump -Fc -d mydb -f mydb.dump
- pg_restore -d newdb mydb.dump
- mongodump --db mydb --out /backups/mongo

### file-and-object-backup
Encrypted incremental file backups and cloud object sync.

**Parameters:**
- `repo` (string): Restic repository reference
- `path` (string): Path to back up

**Commands:**
- `restic init --repo s3:s3.amazonaws.com/bucket/restic`
- `restic backup --repo r: /srv/data`
- `restic snapshots --repo r:`
- `restic restore latest --repo r: --target /restore`
- `rclone copy /srv/data remote:backups --checksum`
- `aws s3 sync /srv/data s3://bucket/backups --delete`

**Examples:**
- restic backup --repo r: /srv/data
- restic snapshots --repo r:
- aws s3 sync /srv/data s3://bucket/backups --delete

## References
- [PostgreSQL Backup Docs](https://www.postgresql.org/docs/current/backup.html)
- [restic Documentation](https://restic.readthedocs.io/)
- [rclone](https://rclone.org/docs/)
- [AWS DR Whitepaper](https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/)