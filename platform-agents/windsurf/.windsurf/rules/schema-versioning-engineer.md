---
trigger: glob
description: "Applies, rolls back, and audits database schema migrations across Flyway, Liquibase, and Atlas with safe deploy workflows. Use when working with flyway migrations, liquibase changesets or when the user mentions flyway migrations, liquibase changesets."
globs: ["**/*.r", "**/*.sh", "**/*.sql"]
---

Applies, rolls back, and audits database schema migrations across Flyway, Liquibase, and Atlas with safe deploy workflows.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `flyway -url=jdbc:postgresql://localhost:5432/appdb -user=app`, `liquibase --changeLogFile=db/changelog.xml update`
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

# Schema Versioning Engineering

Manage database schema evolution with versioned, repeatable, and auditable migrations.

## What This Skill Does

- Author versioned migration scripts (Flyway SQL, Liquibase changelogs, Atlas HCL)
- Applies migrations safely with pre-deploy validation
- Rolls back and repairs migration state
- Diffs schemas to generate new migrations
- Audits migration history across environments

## When to Use

- A new schema change needs to reach production safely
- Migration history is out of sync between environments
- A failed migration needs diagnosis and repair

## Real Commands

```bash
# Flyway
flyway -url=jdbc:postgresql://localhost:5432/appdb -user=app -password=pass migrate
flyway -url=jdbc:postgresql://localhost:5432/appdb info
flyway -url=jdbc:postgresql://localhost:5432/appdb validate
flyway -url=jdbc:postgresql://localhost:5432/appdb repair

# Liquibase
liquibase --changeLogFile=db/changelog.xml update
liquibase status --verbose
liquibase rollback-count 2
liquibase history

# Atlas versioned migrations
atlas migrate diff add_orders_status --dir "file://migrations" --to "file://schema.hcl"
atlas migrate apply --url "postgres://user:pass@localhost:5432/appdb"
atlas migrate status --url "postgres://user:pass@localhost:5432/appdb"
```

## Naming Convention

```text
# Flyway: V<version>__<description>.sql
db/migration/V1__create_customers.sql
db/migration/V2__add_orders_status.sql

# Atlas: atlas migrate diff --dir "file://migrations"
```

## Best Practices

- Never edit an applied migration; add a new version instead
- Make migrations idempotent where possible and reversible when required
- Run validate/status in CI before deploy
- Test migrations against a disposable clone of production data
- Keep schema drift detection (flyway info, atlas migrate status) in the deploy pipeline

## Capabilities

### flyway-migrations
Manage SQL-based migrations with the Flyway CLI.

**Parameters:**
- `url` (string): JDBC URL of the target database
- `locations` (string): Migration script directory, e.g. filesystem:./db/migration
- `target` (string): Migrate up to a specific version, e.g. 1.3

**Commands:**
- `flyway -url=jdbc:postgresql://localhost:5432/appdb -user=app -password=pass migrate`
- `flyway -url=jdbc:postgresql://localhost:5432/appdb info`
- `flyway -url=jdbc:postgresql://localhost:5432/appdb validate`
- `flyway -url=jdbc:postgresql://localhost:5432/appdb repair`
- `flyway -url=jdbc:postgresql://localhost:5432/appdb undo`

**Examples:**
- flyway -url=jdbc:postgresql://localhost:5432/appdb migrate
- flyway -url=jdbc:postgresql://localhost:5432/appdb info
- flyway -url=jdbc:postgresql://localhost:5432/appdb validate

### liquibase-changesets
Create and apply Liquibase changesets and track changelog state.

**Parameters:**
- `changeLogFile` (string): Path to the changelog file
- `count` (string): Number of changesets to roll back

**Commands:**
- `liquibase --changeLogFile=db/changelog.xml update`
- `liquibase status`
- `liquibase rollback-count 2`
- `liquibase diff --changelogFile=db/changelog.xml`
- `liquibase history`

**Examples:**
- liquibase --changeLogFile=db/changelog.xml update
- liquibase status --verbose
- liquibase rollback-count 1

## References
- [Flyway Documentation](https://documentation.red-gate.com/flyway)
- [Liquibase Documentation](https://docs.liquibase.com/home.html)
- [Atlas Migration Docs](https://atlasgo.io/docs/migrations)
