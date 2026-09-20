---
name: "disaster-recovery-disaster-recovery"
description: "Plans and executes disaster recovery for databases and files: RTO/RPO design, pg_dump/restic/rclone backups, and restore drills."
globs: ["**/*.go", "**/*.r", "**/*.sh", "**/*.sql"]
alwaysApply: false
---

# disaster-recovery-disaster-recovery

Plans and executes disaster recovery for databases and files: RTO/RPO design, pg_dump/restic/rclone backups, and restore drills.

## Instructions

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