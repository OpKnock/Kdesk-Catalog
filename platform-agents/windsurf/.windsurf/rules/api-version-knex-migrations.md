---
trigger: glob
description: "Manages database migrations for versioned APIs: knex and Prisma migration workflows, rollback, and schema evolution alongside API versions. Use when working with knex migrations, prisma migrate or when the user mentions knex migrations, prisma migrate."
globs: ["**/*.r", "**/*.sh", "**/*.sql"]
---

Manages database migrations for versioned APIs: knex and Prisma migration workflows, rollback, and schema evolution alongside API versions.

## Agentic Workflow: Read -> Reason -> Act (api-version-knex-migrations)

You are **Api Version Knex Migrations** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `api-version-knex-migrations`
- Domain: Manages database migrations for versioned APIs: knex and Prisma migration workflows, rollback, and schema evolution alongside API versions.
- **knex-migrations**: Create and apply knex migrations — `npx knex migrate:make add_users_table`
- **prisma-migrate**: Manage Prisma schema migrations — `npx prisma migrate dev --name add_users`
- Check `knowledge` and `prerequisites: node.js, python, openapi`

### 2. Reason — think for `api-version-knex-migrations`
- For `knex-migrations`: Create and apply knex migrations — decide which checks to run
- For `prisma-migrate`: Manage Prisma schema migrations — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-version-knex-migrations` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-version-knex-migrations:6f691456`

# API Version v3 - Migrations

Database migrations for API versions.

## What This Skill Does
- Versions database schema changes
- Applies and rolls back migrations
- Keeps schema in sync with API versions

## When to Use
- Schema changes behind new API versions
- Expanding or contracting data models
- Reproducible environments

## Real Commands

```bash
npx knex migrate:make add_users_table
npx knex migrate:latest
npx prisma migrate dev --name add_users
npx prisma migrate deploy
```

## Migration Flow
1. Create the migration
2. Review the generated SQL
3. Apply in staging
4. Deploy schema before code
5. Roll back on failure

## Testing
- Run migrations on a clean database
- Verify rollback restores state
- Test old queries against new schema


## Best Practices
- Deploy migrations before API code
- Make migrations reversible
- Lock migration files per version

## Capabilities

### knex-migrations
Create and apply knex migrations

**Parameters:**
- `name` (string): Migration name
- `directory` (string): Migrations directory
- `environment` (string): Knex env config

**Commands:**
- `npx knex migrate:make add_users_table`
- `npx knex migrate:latest`
- `npx knex migrate:rollback`
- `npx knex migrate:status`
- `npx knex seed:run`

**Examples:**
- knex migrate:make scaffolds a migration
- knex migrate:latest applies pending migrations
- knex migrate:rollback undoes the last batch

### prisma-migrate
Manage Prisma schema migrations

**Commands:**
- `npx prisma migrate dev --name add_users`
- `npx prisma migrate deploy`
- `npx prisma migrate status`
- `npx prisma migrate resolve --applied 20240101000000_add_users`
- `npx prisma generate`

**Examples:**
- -cli --help
- -api --help

## References
- [Knex Migrations](https://knexjs.org/guide/migrations.html)
- [Prisma Migrate](https://www.prisma.io/docs/orm/prisma-migrate)
