---
applyTo: "**/*.json **/*.r **/*.sh **/*.sql"
---

# database-migration-database-2

Version-controlled database schema changes with Flyway and Liquibase: migrate, validate, and rollback.

## Instructions

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
