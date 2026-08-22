---
applyTo: "**/*.json **/*.r **/*.sh **/*.sql"
---

# idempotency-designer-idempotency-designer

Designs idempotent APIs and consumers: idempotency keys, Redis SETNX locks, unique constraints, and replay-safe workflows.

## Instructions

# Idempotency Design

Make writes safe to retry without double effects.

## When to Use

- Payment and order APIs where clients retry
- Webhook consumers that redeliver events
- Queue workers with at-least-once delivery

## Idempotency key pattern

1. Client sends `Idempotency-Key` header.
2. Server tries `SET key status NX EX 900` in Redis.
3. If key exists, return the stored response instead of re-processing.

```bash
redis-cli SET charge:key:abc 202 accepted NX EX 300
redis-cli GET charge:key:abc
```

If NX fails, load the stored response and return it with 200.

## Key rules

- Keys must be unique per logical operation, random per client.
- TTL the lock (300-900s) to bound storage.
- Return the same response body for replays - clients compare it.

## Database uniqueness

Add a unique constraint as the source of truth:

```sql
CREATE UNIQUE INDEX uq_payment_request
  ON payments(request_id) WHERE status <> 'failed';
```

## Testing replays

```bash
curl -i -X POST http://localhost:8080/orders -H 'Idempotency-Key: abc-123' -d '{"sku":"A1"}'
curl -i -X POST http://localhost:8080/orders -H 'Idempotency-Key: abc-123' -d '{"sku":"A1"}'
```

The second call must not create a second order.

## Concurrency test

```js
// idempotency-test.js
import http from 'k6/http';
const key = 'k6-' + Date.now();

export default function () {
  http.post('http://localhost:8080/orders',
    JSON.stringify({ sku: 'A1' }),
    { headers: { 'Idempotency-Key': key, 'Content-Type': 'application/json' } });
}
```

```bash
k6 run --vus 20 --duration 10s idempotency-test.js
```

Exactly one order must be created despite 20 concurrent requests.

## Best practices

- Log the idempotency key with every write for audit.
- Never reuse a key with different payloads.
- Test that failures during processing do not poison the lock.

## Testing

Run sequential replay tests and the k6 concurrency test in CI.

## Capabilities

### redis-locks
Implement idempotency keys with Redis atomic primitives.

**Commands:**
- `redis-cli SET order:key:abc123 processed NX EX 900`
- `redis-cli SETNX order:key:abc123 processed`
- `redis-cli GET order:key:abc123`
- `redis-cli EXPIRE order:key:abc123 900`
- `redis-cli EVAL "if redis.call('GET', KEYS[1]) == ARGV[1] then redis.call('DEL', KEYS[1]) return 1 else return 0 end" 1 order:key:abc123 done`

**Examples:**
- redis-cli SET charge:key:xyz 202 accepted NX EX 300
- redis-cli --eval lua/check-and-set.lua order:key:abc123 , request-id-1
- redis-cli GET charge:key:xyz

### api-tests
Verify idempotent behavior against live APIs.

**Commands:**
- `curl -i -X POST http://localhost:8080/orders -H 'Idempotency-Key: abc-123' -H 'Content-Type: application/json' -d '{"sku":"A1"}'`
- `curl -i -X POST http://localhost:8080/orders -H 'Idempotency-Key: abc-123' -H 'Content-Type: application/json' -d '{"sku":"A1"}'`
- `curl -i -X POST http://localhost:8080/orders -H 'Idempotency-Key: abc-456' -H 'Content-Type: application/json' -d '{"sku":"A1"}'`
- `k6 run --vus 20 --duration 10s idempotency-test.js`
- `ab -n 200 -c 20 -p payload.json -T application/json -H 'Idempotency-Key: load-test-1' http://localhost:8080/orders`

**Examples:**
- curl -i -X POST http://localhost:8080/payments -H 'Idempotency-Key: pay-1' -d '{"amount":100}' | head -12
- k6 run --vus 50 --duration 10s idempotency-test.js
- curl -i -X DELETE http://localhost:8080/orders/42
