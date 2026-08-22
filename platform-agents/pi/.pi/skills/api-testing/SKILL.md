---
name: "api-testing"
description: "Tests REST APIs with curl, httpie, and Newman, covering auth, contracts, and response validation from the terminal."
---

# api-testing

Tests REST APIs with curl, httpie, and Newman, covering auth, contracts, and response validation from the terminal.

## Instructions

# API Testing

Test REST APIs quickly from the terminal with curl, httpie, and Newman.

## What This Skill Does

- Exercises endpoints with status and body assertions
- Verifies auth, headers, and contract fields
- Runs Postman collections in CI with data files
- Generates HTML/CLI reports

## When to Use

- Quick smoke tests of a new endpoint
- Contract verification before merge
- CI regression suites for APIs

## Real Commands

```bash
# curl
curl -s -o /dev/null -w '%{http_code}' https://api.example.com/v1/users
curl -s -X POST https://api.example.com/v1/users -H 'Content-Type: application/json' -d '{"name":"alice"}'
curl -s https://api.example.com/v1/users | jq -e '.data | length > 0'

# httpie
http GET https://api.example.com/v1/users
http POST https://api.example.com/v1/users name=alice role=admin
http -h GET https://api.example.com/v1/users

# Newman
newman run collection.json -e staging.postman_environment.json
newman run collection.json -d data.csv -r html,cli --reporter-html-export report.html
```

## Assertion Pattern (Newman script)

```js
pm.test("returns 201 and user id", () => {
  pm.response.to.have.status(201);
  const body = pm.response.json();
  pm.expect(body.data.id).to.be.a('string');
});
```

## Best Practices

- Assert status AND schema, not just 200
- Keep tests independent; create resources in setup scripts
- Use environment variables for base URLs and tokens
- Run collections with data files for data-driven cases
- Fail CI on HTTP 5xx or schema drift

## Capabilities

### curl-testing
Craft and assert on API requests with curl.

**Commands:**
- `curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/v1/users`
- `curl -s -X POST http://localhost:8080/v1/users -H 'Content-Type: application/json' -d '{"name":"alice"}'`
- `curl -s http://localhost:8080/v1/users | jq -e '.data | length > 0'`
- `curl -sI http://localhost:8080/v1/health`
- `curl -s -u user:pass http://localhost:8080/v1/users`

**Examples:**
- curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/v1/users
- curl -s -X POST http://localhost:8080/v1/users -H 'Content-Type: application/json' -d '{"name":"alice"}' | jq .
- curl -s http://localhost:8080/v1/users | jq -e '.data | length > 0'

### httpie-testing
Human-friendly API testing with httpie.

**Commands:**
- `http GET http://localhost:8080/v1/users`
- `http POST http://localhost:8080/v1/users name=alice role=admin`
- `http --json POST http://localhost:8080/v1/users <<< '{"name":"bob"}'`
- `http -h GET http://localhost:8080/v1/users`
- `http GET http://localhost:8080/v1/users Authorization:'Bearer $TOKEN'`

**Examples:**
- http GET http://localhost:8080/v1/users
- http POST http://localhost:8080/v1/users name=alice role=admin
- http -h GET http://localhost:8080/v1/users

### newman-collections
Run Postman collections with assertions in CI.

**Commands:**
- `newman run api.postman_collection.json`
- `newman run collection.json -e staging.postman_environment.json`
- `newman run collection.json -d data.csv`
- `newman run collection.json -r html,cli --reporter-html-export report.html`
- `newman run collection.json --env-var baseUrl=http://localhost:8080`

**Examples:**
- newman run collection.json -e staging.env.json
- newman run collection.json -r html,cli --reporter-html-export report.html
- newman run collection.json --env-var baseUrl=http://localhost:8080
