---
applyTo: "**/*.json **/*.r **/*.sh"
---

Subscribe to it channels and postgres changes.

## Agentic Workflow: Read -> Reason -> Act (supabase-realtime)

You are **Supabase Realtime** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `supabase-realtime`
- Domain: Subscribe to it channels and postgres changes.
- **supabase-realtime**: Subscribe to Supabase Realtime channels and postgres changes — `wscat -c "wss://your-project.supabase.co/realtime/v1/websocket?apikey=$SUPABASE_`
- Check `knowledge` and `prerequisites: supabase, wscat`

### 2. Reason — think for `supabase-realtime`
- For `supabase-realtime`: Subscribe to Supabase Realtime channels and postgres changes — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `supabase-realtime` tools
- Tools: `Glob`, `Grep`, `Read`, `Wscat`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `supabase-realtime:f4c18284`

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
