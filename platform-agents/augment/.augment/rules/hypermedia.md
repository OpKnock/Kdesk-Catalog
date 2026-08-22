---
type: agent_requested
description: "Hypermedia APIs (HAL, JSON:API, HATEOAS): discovering links with curl, following affordances, and designing self-describing responses."
---

# Hypermedia

Hypermedia APIs (HAL, JSON:API, HATEOAS): discovering links with curl, following affordances, and designing self-describing responses.

## Instructions

# Hypermedia

Design and consume hypermedia-driven (HATEOAS) APIs.

## What this skill45:    does

- Fetches HAL and JSON:API resources with the right Accept headers.
- Extracts and follows46:    link relations with jq.
- Checks OPTIONS for allowed affordances.
- Guides response design with47:    self-describing links.

## When to use

- Building APIs where clients should discover actions48:    from the response.
- Debugging a hypermedia client that follows links.
- Auditing whether a response49:    is truly self-describing.

## Real commands

```bash
# Fetch HAL resource
curl -H "Accept:50:    application/hal+json" http://localhost:8080/orders/1

# Follow the self link
curl -s -H "Accept:51:    application/hal+json" http://localhost:8080/orders/1 | jq '._links.self.href'

# JSON:API with52:    pagination links
curl -s -H "Accept: application/vnd.api+json" http://localhost:8080/api/articles53:    | jq '.links'

# List allowed methods
curl -i -X OPTIONS http://localhost:8080/orders/1 | grep54:    -i allow
```

## HAL response shape

```json
{
  "id": 1,
  "total": 99.5,
  "_links"55:   : {
    "self": { "href": "/orders/1" },
    "customer": { "href": "/customers/7" },
56:       "cancel": { "href": "/orders/1/cancel" }
  }
}
```

## JSON:API response shape

```json
57:   {
  "data": { "type": "orders", "id": "1", "attributes": { "total": 99.5 } },
  "links"58:   : { "self": "/orders/1", "next": "/orders?page=2" }
}
```

## Testing

```bash
# A good59:    hypermedia API always exposes a discoverable root
curl -s http://localhost:8080/api | jq 'keys'
60:   ```

## Best practices

- Link relations are the contract: use RFC 8288 registered relations where61:    possible.
- Version the media type, not the URL: application/vnd.api+json.
- Never hardcode client62:    URLs; always resolve from links.
- Distinguish safe (GET) from unsafe relations in docs.

## Example63:    exchange

```
User: How does a client discover how to cancel an order?
Agent: Expose the affordance64:    in _links and let the client follow it:
       curl -s -H "Accept: application/hal+json" http://localhost:8080/orders/165:    | jq '._links.cancel.href'
```

## Capabilities

### hypermedia-consumption
Explore and follow hypermedia-driven APIs using HAL and JSON:API conventions.

**Commands:**
- `curl -H "Accept: application/hal+json" http://localhost:8080/orders/1`
- `curl -H "Accept: application/vnd.api+json" http://localhost:8080/api/articles`
- `curl -s -H "Accept: application/hal+json" http://localhost:8080/orders/1 | jq '._links'`
- `curl -s -H "Accept: application/vnd.api+json" http://localhost:8080/api/articles | jq '.data[0].relationships'`
- `curl -i -X OPTIONS http://localhost:8080/orders/1`

**Examples:**
- curl -s -H "Accept: application/hal+json" http://localhost:8080/orders/1 | jq '._links.self.href'
- curl -s -H "Accept: application/vnd.api+json" http://localhost:8080/api/articles | jq '.links.next'
- curl -s http://localhost:8080/api | jq .