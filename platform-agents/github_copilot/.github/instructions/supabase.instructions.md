---
applyTo: "**/*.r **/*.sh **/*.sql"
---

# supabase

Builds apps with Supabase: local development, migrations, auth, storage, and database operations with the supabase CLI.

## Instructions

# Supabase

Backend-as-a-service on Postgres.

## When to Use

- Postgres-backed apps without server management
- Auth (email, OAuth) and Row Level Security
- Storage buckets for user files
- Edge functions for custom logic

## Commands

```bash
# Local stack
npx supabase init
npx supabase start
npx supabase status
npx supabase stop
npx supabase db reset

# Migrations
npx supabase migration new create_users
npx supabase db push
npx supabase db diff -f users_table --linked
npx supabase migration list

# Link to a hosted project
npx supabase link --project-ref abcdef
npx supabase projects list

# Functions
npx supabase functions serve
npx supabase functions deploy myfunc

# Storage
npx supabase storage create-bucket avatars --public
```

## Best Practices

- Do all schema work via migrations, never ad-hoc SQL in prod
- Use RLS policies for row-level security by default
- Keep the local stack in sync with prod via db diff
- Run supabase functions serve for local edge function dev
- Rotate service role keys; use anon key on clients
- Reset local DB from migrations, not snapshots

## Capabilities

### supabase-local
Run the local Supabase stack.

**Commands:**
- `npx supabase init`
- `npx supabase start`
- `npx supabase stop`
- `npx supabase status`
- `npx supabase db reset`

**Examples:**
- npx supabase start --exclude auth
- npx supabase status -o env
- npx supabase stop --no-backup

### supabase-db
Manage migrations and database operations.

**Commands:**
- `npx supabase migration new create_users`
- `npx supabase db push`
- `npx supabase db diff --linked`
- `npx supabase db lint`
- `psql "postgresql://postgres:postgres@localhost:54322/postgres" -c "SELECT 1"`

**Examples:**
- npx supabase db diff -f users_table --linked
- npx supabase migration list
- npx supabase db reset --no-seed

### supabase-auth-storage
Manage auth users, storage buckets, and functions.

**Commands:**
- `npx supabase functions deploy myfunc`
- `npx supabase functions serve`
- `npx supabase storage create-bucket avatars --public`
- `npx supabase projects list`
- `npx supabase link --project-ref abcdef`

**Examples:**
- npx supabase functions deploy myfunc --project-ref abcdef
- npx supabase storage empty-bucket avatars
- npx supabase projects list
