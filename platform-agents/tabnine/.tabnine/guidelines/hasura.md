# hasura

Operates Hasura GraphQL engines: metadata management, migrations, console access, remote schemas, and permissions.

## Instructions

# Hasura

Instant GraphQL APIs on top of Postgres.

## When to Use

- Auto-generated GraphQL CRUD over existing Postgres
- Permission-driven multi-tenant data access
- Composing remote schemas and actions
- Event-driven data (webhooks, cron) on database events

## Commands

```bash
# Init and console
hasura init myproject --endpoint http://localhost:8080
hasura console

# Migrations
hasura migrate create init --from-server
hasura migrate apply
hasura migrate status

# Metadata
hasura metadata export
hasura metadata apply
hasura metadata reload

# Seeds
hasura seed create users
hasura seed apply

# Engine health
curl -s http://localhost:8080/healthz

# Run SQL via the metadata API
curl -X POST http://localhost:8080/v1/query \
  -H "x-hasura-admin-secret: mysecret" -H "Content-Type: application/json" \
  -d '{"type":"run_sql","args":{"sql":"SELECT version();"}}'
```

## Best Practices

- Manage schema via migrations, metadata via version control
- Never ship the admin secret in client code
- Use permissions/roles per consumer instead of one super-user
- Track Hasura version to plan upgrades
- Use remote schemas for non-Postgres data
- Apply metadata in CI and verify with a schema diff

## Capabilities

### hasura-cli
Manage Hasura metadata and migrations.

**Commands:**
- `hasura init myproject --endpoint http://localhost:8080`
- `hasura console`
- `hasura migrate create init --from-server`
- `hasura migrate apply`
- `hasura metadata export`

**Examples:**
- hasura init --endpoint http://localhost:8080 --admin-secret mysecret
- hasura metadata apply --project myproject
- hasura migrate status

### graphql-engine
Query the GraphQL engine and manage schema.

**Commands:**
- `curl -X POST http://localhost:8080/v1/graphql -H "x-hasura-admin-secret: mysecret" -H "Content-Type: application/json" -d "{\"query\":\"{ __schema { types { name } } }\"}"`
- `curl -X POST http://localhost:8080/v1/query -H "x-hasura-admin-secret: mysecret" -H "Content-Type: application/json" -d "{\"type\":\"run_sql\",\"args\":{\"sql\":\"SELECT version();\"}}"`
- `hasura metadata reload`
- `hasura seed create users`

**Examples:**
- curl -s http://localhost:8080/healthz
- hasura seed apply