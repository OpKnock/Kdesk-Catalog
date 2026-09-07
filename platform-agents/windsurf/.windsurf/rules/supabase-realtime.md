---
trigger: glob
description: "Subscribe to it channels and postgres changes. Use when working with supabase realtime, api or when the user mentions supabase realtime, api."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

Subscribe to it channels and postgres changes.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `wscat -c "wss://your-project.supabase.co/realtime/v1/websock`
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

# Supabase Realtime

Hand-crafted skill for live data with Supabase Realtime.

## What this skill does

- Connects to the Realtime websocket with wscat for manual inspection
- Subscribes to postgres_changes events on tables
- Triggers and verifies INSERT events end to end

## When to use

- Live feeds: orders, chat, presence, leaderboards
- Debugging why a client does not receive row changes
- Prototyping before writing client SDK code

## Real commands

```bash
# Raw websocket connection (then send subscribe JSON)
wscat -c "wss://your-project.supabase.co/realtime/v1/websocket?apikey=$SUPABASE_ANON_KEY&vsn=1.0.0"

# Trigger an INSERT through PostgREST (fires postgres_changes)
curl -X POST 'https://your-project.supabase.co/rest/v1/orders' -H "apikey: $SUPABASE_ANON_KEY" -H 'Content-Type: application/json' -H 'Prefer: return=representation' -d '{"qty":2}'

# Migrate schema changes that define the tables
supabase db push

# Read back rows
curl -s 'https://your-project.supabase.co/rest/v1/orders?select=*&order=created_at.desc' -H "apikey: $SUPABASE_ANON_KEY" | jq '.[0]'
```

## Subscribe message

```json
{
  "topic": "realtime:orders",
  "event": "phx_join",
  "payload": {
    "config": {
      "postgres_changes": [{ "event": "INSERT", "schema": "public", "table": "orders" }]
    }
  }
}
```

## Testing

```bash
# Terminal A: wscat to the websocket, send the subscribe message
# Terminal B: POST an INSERT; watch Terminal A print the change event
curl -X POST 'https://your-project.supabase.co/rest/v1/orders' -H "apikey: $KEY" -H 'Prefer: return=representation' -d '{"qty":3}'
```

## Best practices

- Subscribe only to events you need: INSERT vs * changes payload size
- Use RLS-aware replication so users only see allowed rows
- Prefer the SDK's onPostgresChanges over raw websockets in apps

## Capabilities

### supabase-realtime
Subscribe to Supabase Realtime channels and postgres changes

**Parameters:**
- `channel` (string): Realtime channel name, e.g. postgres_changes
- `table` (string): Table to subscribe to, e.g. orders
- `event` (string): INSERT, UPDATE, DELETE, or *

**Commands:**
- `wscat -c "wss://your-project.supabase.co/realtime/v1/websocket?apikey=$SUPABASE_ANON_KEY&vsn=1.0.0"`
- `curl -X POST 'https://your-project.supabase.co/rest/v1/orders' -H "apikey: $SUPABASE_ANON_KEY" -H "Authorization: Bearer $SUPABASE_ANON_KEY" -H 'Content-Type: application/json' -H 'Prefer: return=representation' -d '{"qty":2}'`
- `supabase db push`
- `curl -s 'https://your-project.supabase.co/rest/v1/orders?select=*&order=created_at.desc' -H "apikey: $SUPABASE_ANON_KEY" | jq '.[0]'`

**Examples:**
- wscat -c "wss://your-project.supabase.co/realtime/v1/websocket?apikey=$SUPABASE_ANON_KEY&vsn=1.0.0"
- curl -X POST 'https://your-project.supabase.co/rest/v1/orders' -H "apikey: $KEY" -H 'Prefer: return=representation' -d '{"qty":2}'
- supabase db push

## References
- [Supabase Realtime docs](https://supabase.com/docs/guides/realtime)
- [Realtime protocol](https://supabase.com/docs/guides/realtime/protocol)
