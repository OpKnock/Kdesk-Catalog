# Api Integration Event Driven

Designs integration architectures: event-driven patterns, webhook contracts, retry and queue designs for third-party APIs.

## Instructions

# API Integration (Design)

Designs robust integration architecture before writing connector code.

## When to Use
- New integration needs reliability design
- Events must survive crashes
- Retry policies need modeling

## Real Commands

```bash
# Queue events
redis-cli LPUSH integration.events '{"type":"order.created"}'
redis-cli BRPOP integration.events 0

# Streams for audit-able events
redis-cli XADD stream:orders '*' type order.created
redis-cli XREAD COUNT 5 STREAMS stream:orders 0

# Idempotency keys
redis-cli SET idem:charge_1 'done' NX EX 86400
```

## Backoff Design
Exponential with jitter: `2^n * 100ms + random`.

## Webhook Contract
- Signature header on every delivery
- Retries with exponential backoff
- Exactly-once via event IDs

## Testing
Kill the consumer mid-stream and verify replay from the last acked position.

## Best Practices
- Design for at-least-once delivery
- Make every handler idempotent

## Capabilities

### event-driven-design
Model pub/sub flows and queues for integration workloads

**Commands:**
- `redis-cli LPUSH integration.events '{"type":"order.created"}'`
- `redis-cli BRPOP integration.events 0`
- `redis-cli LLEN integration.events`
- `redis-cli XADD stream:orders '*' type order.created`
- `redis-cli XREAD COUNT 5 STREAMS stream:orders 0`

**Examples:**
- redis-cli LPUSH integration.events '{"type":"order.created"}' && redis-cli BRPOP integration.events 0
- redis-cli XADD stream:orders '*' type order.created
- redis-cli XREAD COUNT 5 STREAMS stream:orders 0

### retry-design
Design retry and backoff strategies for upstream APIs

**Commands:**
- `node -e "const backoff=[100,250,500];const f=(tries)=>backoff[Math.min(tries,backoff.length-1)];console.log([0,1,2,3].map(f))"`
- `node -e "const jitter=(base)=>base*0.5+Math.random()*base;console.log([1,2,3].map(i=>jitter(2**i*100)))"`
- `curl -s -o /dev/null -w '%{http_code} %{time_total}s\n' -X POST http://localhost:3000/integrations/payment -H 'Idempotency-Key: test-1'`
- `redis-cli SET idem:charge_1 'done' NX EX 86400`
- `node -e "console.log('circuit states: closed|open|half-open')"`

**Examples:**
- node -e "const backoff=[100,250,500];const f=(tries)=>backoff[Math.min(tries,backoff.length-1)];console.log([0,1,2,3].map(f))"
- curl -s -o /dev/null -w '%{http_code} %{time_total}s\n' -X POST http://localhost:3000/integrations/payment -H 'Idempotency-Key: test-1'
- redis-cli SET idem:charge_1 'done' NX EX 86400
