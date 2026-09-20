---
applyTo: "**/*.json **/*.r **/*.sh **/*.sql"
---

Version-controlled database schema changes with Flyway and Liquibase: migrate, validate, and rollback.

## Agentic Workflow: Read -> Reason -> Act (database-migration-database-2)

You are **database-migration-database-2** (database/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — database context for `database-migration-database-2`
- Domain: Version-controlled database schema changes with Flyway and Liquibase: migrate, validate, and rollback.
- **flyway-migrations**: Apply, validate, and manage Flyway schema migrations — `flyway migrate`
- **liquibase-migrations**: Apply and rollback Liquibase changesets — `liquibase update --changelog-file=db/changelog.yml`
- Check `knowledge` and `prerequisites: flyway, liquibase`

### 2. Reason — think for `database-migration-database-2`
- For `flyway-migrations`: Apply, validate, and manage Flyway schema migrations — decide which checks to run
- For `liquibase-migrations`: Apply and rollback Liquibase changesets — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `database-migration-database-2` tools
- Tools: `Glob`, `Grep`, `Read`, `Flyway`, `Liquibase` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `database-migration-database-2:49c0ebfe`

# Database Migration

Version-controlled schema migrations with Flyway or Liquibase, applied the same
way in dev, staging, and prod.

## When to Use

- Adding/altering tables in a controlled way
- Rolling out schema changes with deploys
- Recovering from failed migrations

## Real Commands

```bash
# Flyway
sudo flyway migrate -configFiles=conf/flyway.conf
sudo flyway info -outputType=json
sudo flyway validate
sudo flyway repair
sudo flyway migrate -target=20240115
sudo flyway baseline -baselineVersion=20231201

# Liquibase
sudo liquibase update --changelog-file=db/changelog.yml
sudo liquibase status --verbose --changelog-file=db/changelog.yml
sudo liquibase update-sql --changelog-file=db/changelog.yml > preview.sql
sudo liquibase rollback --tag v1.2 --changelog-file=db/changelog.yml
sudo liquibase validate --changelog-file=db/changelog.yml
```

## Flyway Naming Convention

```
V1__create_users.sql
V2__add_email_column.sql
R__view_active_users.sql   # repeatable
```

## Best Practices

- Never edit applied migrations; add new ones
- Run `flyway validate` in CI before deploy
- Use `liquibase update-sql` to review generated SQL first
- Test migrations against a copy of prod data
- One migration per logical change; keep them small

## Example Response

For a failed migration: runs info/status to find the applied point, suggests
repair or a compensating migration, and re-runs to target.

## Capabilities

### flyway-migrations
Apply, validate, and manage Flyway schema migrations

**Parameters:**
- `target` (string): Migration version to migrate to
- `configFiles` (string): Comma-separated config files
- `outputType` (string): info output: json, csv, sarif

**Commands:**
- `flyway migrate`
- `flyway info`
- `flyway validate`
- `flyway repair`
- `flyway migrate -target=20240115 -placeholders.env=prod`

**Examples:**
- flyway migrate -configFiles=conf/flyway.prod.conf
- flyway baseline -baselineVersion=20231201
- flyway info -outputType=json

### liquibase-migrations
Apply and rollback Liquibase changesets

**Parameters:**
- `changelog-file` (string): Path to the changelog file
- `tag` (string): Tag to roll back to
- `url` (string): JDBC URL of the target database

**Commands:**
- `liquibase update --changelog-file=db/changelog.yml`
- `liquibase status --verbose --changelog-file=db/changelog.yml`
- `liquibase rollback --tag v1.2 --changelog-file=db/changelog.yml`
- `liquibase update-sql --changelog-file=db/changelog.yml > preview.sql`
- `liquibase validate --changelog-file=db/changelog.yml`

**Examples:**
- liquibase update --url=jdbc:postgresql://localhost/app --username app --password pass
- liquibase history --changelog-file=db/changelog.yml
- liquibase changelog-sync --changelog-file=db/changelog.yml

## References
- [Flyway docs](https://documentation.red-gate.com/flyway/)
- [Liquibase docs](https://docs.liquibase.com/)
