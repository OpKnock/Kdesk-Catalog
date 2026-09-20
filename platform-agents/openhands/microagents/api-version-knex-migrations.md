---
name: "api-version-knex-migrations"
description: "Manages database migrations for versioned APIs: knex and Prisma migration workflows, rollback, and schema evolution alongside API versions."
type: knowledge
triggers: ["api-version-knex-migrations", "knex-migrations", "prisma-migrate"]
---

# Api Version Knex Migrations

Manages database migrations for versioned APIs: knex and Prisma migration workflows, rollback, and schema evolution alongside API versions.

## Instructions

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
