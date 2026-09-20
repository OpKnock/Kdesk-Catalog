# Cqrs

Implement Command Query Responsibility Segregation with EventStoreDB: append events, project read models, and query them.

## Instructions

# CQRS

Separate writes (commands) from reads (queries) with event sourcing.

## When to Use

- Read-heavy APIs where the write model is not query-friendly
- Event-driven systems with audit requirements
- Scaling reads independently from writes

## Start EventStoreDB

```bash
docker run -d --name eventstore -p 2113:2113 eventstore/eventstore:latest --insecure
```

## Append Events (Commands)

```bash
curl -X POST http://localhost:2113/streams/order-1 \
  -H "Content-Type: application/json" \
  -H "ES-EventType: OrderPlaced" \
  -H "ES-EventId: $(uuidgen)" \
  -d '{"data":{"amount":100}}'
```

Use ES-ExpectedVersion for optimistic concurrency on commands.

## Read Events (Queries)

```bash
curl http://localhost:2113/streams/order-1 -H "Accept: application/json" | jq '.entries[].eventType'
curl http://localhost:2113/streams/order-1 -H "Accept: application/json" | jq '.entries[].data'
```

## Projections (Read Models)

```json
{
  "name": "order-totals",
  "type": "JS",
  "enabled": true,
  "query": "fromAll().when({ OrderPlaced: function(s, e) { s.total = (s.total || 0) + e.data.amount; return s; } })"
}
```

```bash
curl -X POST http://localhost:2113/projections/continuous \
  -H "Content-Type: application/json" -H "ES-ExpectedVersion: -1" -d @projection.json
curl http://localhost:2113/projection/order-totals/state -H "Accept: application/json"
```

## Testing

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:2113/streams/order-1
curl -s http://localhost:2113/streams/order-1 -H "Accept: application/json" | jq '.entries | length'
```

## Best Practices

- Never store mutable state as the source of truth; events are
- Use ES-ExpectedVersion to prevent write conflicts
- Build read models via projections or materialized views
- Query the read model, never the event store
- Version events for schema evolution

## Capabilities

### eventstore
Run EventStoreDB and append/read events via its HTTP API

**Commands:**
- `docker run -d --name eventstore -p 2113:2113 eventstore/eventstore:latest --insecure`
- `curl -X POST http://localhost:2113/streams/order-1 -H "Content-Type: application/json" -H "ES-EventType: OrderPlaced" -H "ES-EventId: $(uuidgen)" -d '{"data":{"amount":100}}'`
- `curl http://localhost:2113/streams/order-1 -H "Accept: application/json"`
- `curl -X POST http://localhost:2113/streams/order-1 -H "Content-Type: application/json" -H "ES-ExpectedVersion: 0" -H "ES-EventType: OrderPaid" -H "ES-EventId: $(uuidgen)" -d '{"data":{"paid":true}}'`

**Examples:**
- curl -X POST http://localhost:2113/streams/order-1 -H "Content-Type: application/json" -H "ES-EventType: OrderPlaced" -H "ES-EventId: $(uuidgen)" -d '{"data":{"amount":100}}'
- curl http://localhost:2113/streams/order-1 -H "Accept: application/json" | jq '.entries[].eventType'
- curl -s http://localhost:2113/streams/order-1 -H "Accept: application/vnd.eventstore.atom+json" | jq '.entries | length'

### read-models
Project events into queryable read models and consume streams

**Commands:**
- `curl http://localhost:2113/streams/order-1 -H "Accept: application/json" | jq '.entries[].data'`
- `curl -X POST http://localhost:2113/projections/continuous -H "Content-Type: application/json" -H "ES-ExpectedVersion: -1" -d @projection.json`
- `curl http://localhost:2113/projection/order-totals/state -H "Accept: application/json"`
- `curl http://localhost:2113/streams/order-1/-1/backward/10 -H "Accept: application/json"`

**Examples:**
- curl http://localhost:2113/projection/order-totals/state -H "Accept: application/json" | jq '.total'
- curl http://localhost:2113/streams/order-1 -H "Accept: application/json" | jq '.entries[].data'
- curl -s -o /dev/null -w "%{http_code}" http://localhost:2113/streams/order-1