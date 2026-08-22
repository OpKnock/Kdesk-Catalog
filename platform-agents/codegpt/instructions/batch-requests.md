# Batch Requests

Combines multiple API calls into single HTTP round trips using JSON-RPC batch arrays, GraphQL operation aliases, and dedicated batch endpoints to reduce client-side latency over high-latency networks.

## Instructions

# Batch Requests

## What this skill does

Combines multiple API calls into single HTTP round trips using JSON-RPC batch arrays, GraphQL operation aliases, and dedicated batch endpoints to reduce client-side latency over high-latency networks.

## When to use

- Clients make many small calls that can be grouped
- Reducing round trips over high-latency networks
- Bulk reads or writes in one operation

## Real commands

```bash
# JSON-RPC batch
curl -X POST http://localhost:8545 -H "Content-Type: application/json" -d '[{"jsonrpc":"2.0","method":"eth_blockNumber","id":1},{"jsonrpc":"2.0","method":"eth_chainId","id":2}]'

# GraphQL batch (JSON array of operations)
curl -X POST https://api.your-app.test/graphql -H "Content-Type: application/json" -d '[{"query":"{users{id}}"},{"query":"{posts{id}}"}]'

# Dedicated batch endpoint
curl -X POST https://api.your-app.test/batch -H "Content-Type: application/json" -d '{"requests":[{"path":"/users/1","method":"GET"},{"path":"/posts","method":"GET"}]}'
```

## Testing

- Compare time_total for N single calls vs one batch call
- Assert per-item status codes in the batch response

## Best practices

- Cap batch sizes to bound server work (e.g. 100 items)
- Return per-item errors, not all-or-nothing
- Use id/alias mapping so clients can correlate responses
- Batch only idempotent or cache-friendly reads by default

## Capabilities

### jsonrpc-batch
Send batched JSON-RPC requests.

**Commands:**
- `curl -X POST http://localhost:8545 -H "Content-Type: application/json" -d '[{"jsonrpc":"2.0","method":"eth_blockNumber","id":1},{"jsonrpc":"2.0","method":"eth_chainId","id":2}]'`
- `curl -X POST https://api.your-app.test/rpc -H "Content-Type: application/json" -d '[{"jsonrpc":"2.0","method":"getUser","params":[1],"id":1},{"jsonrpc":"2.0","method":"getOrder","params":[42],"id":2}]'`
- `jq -c '.[]' batch.json | while read r; do curl -s -X POST https://api.your-app.test/rpc -d "$r"; done`

**Examples:**
- curl -X POST http://localhost:8545 -H "Content-Type: application/json" -d '[{"jsonrpc":"2.0","method":"eth_blockNumber","id":1},{"jsonrpc":"2.0","method":"eth_chainId","id":2}]'
- curl -s -X POST https://api.your-app.test/rpc -H "Content-Type: application/json" -d '[{"jsonrpc":"2.0","method":"getUser","params":[1],"id":1}]' | jq .
- jq -c '.[]' batch.json | xargs -I{} curl -s -X POST https://api.your-app.test/rpc -H 'Content-Type: application/json' -d '{}'

### graphql-batching
Execute multiple GraphQL operations in one HTTP round trip.

**Commands:**
- `curl -X POST https://api.your-app.test/graphql -H "Content-Type: application/json" -d '[{"query":"{users{id}}"},{"query":"{posts{id}}"}]'`
- `curl -X POST https://api.your-app.test/graphql -H "Content-Type: application/json" -d '{"query":"query { users { id } posts { id } }"}'`
- `curl -s -X POST https://api.your-app.test/graphql -H "Content-Type: application/json" -d '{"query":"{ a: users { id } b: posts { id } }"}'`

**Examples:**
- curl -X POST https://api.your-app.test/graphql -H "Content-Type: application/json" -d '[{"query":"{users{id}}"},{"query":"{posts{id}}"}]'
- curl -s -X POST https://api.your-app.test/graphql -H "Content-Type: application/json" -d '{"query":"query A { users { id } } query B { posts { id } }"}'
- curl -s -X POST https://api.your-app.test/graphql -H "Content-Type: application/json" -d '{"query":"{ a: users { id } b: posts { id } }"}' | jq '.data | keys'

### server-batch
Create and test dedicated batch endpoints.

**Commands:**
- `curl -X POST https://api.your-app.test/batch -H "Content-Type: application/json" -d '{"requests":[{"path":"/users/1","method":"GET"},{"path":"/posts","method":"GET"}]}'`
- `curl -s -o /dev/null -w "%{http_code} %{time_total}\n" -X POST https://api.your-app.test/batch -H "Content-Type: application/json" -d '{"requests":[{"path":"/users/1","method":"GET"}]}'`
- `curl -s -X POST https://api.your-app.test/batch -H "Content-Type: application/json" -d '{"requests":[{"path":"/users/1","method":"GET"}]}' | jq '.responses | length'`

**Examples:**
- curl -s -X POST https://api.your-app.test/batch -H "Content-Type: application/json" -d '{"requests":[{"path":"/users/1","method":"GET"},{"path":"/users/2","method":"GET"}]}'
- curl -s -X POST https://api.your-app.test/batch -H "Content-Type: application/json" -d '{"requests":[{"path":"/users","method":"POST","body":{"name":"x"}}]}' | jq '.responses[0].status'
- curl -s -X POST https://api.your-app.test/batch -H "Content-Type: application/json" -d '{"requests":[]}'
