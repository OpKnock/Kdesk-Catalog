# api-pagination-specialist

Implements RFC 8288 Link headers for pagination: rel=next/prev/first/last, parsing with standard libraries, and REST hypermedia navigation.

## Instructions

# API Pagination Specialist

Link-header pagination per RFC 8288.

## What This Skill Does
- Emits next/prev/first/last URLs in the Link response header
- Keeps pagination metadata out of the response body
- Enables generic hypermedia-driven clients

## When to Use
- REST APIs with clients that follow Link relations
- Standardizing pagination across many endpoints
- Paginating where the body shape must stay fixed

## Real Commands

```bash
curl -s -D- 'http://api.example.com/users?page=2' | grep -i '^link:'
npm install parse-link-header
node -e "const parse=require('parse-link-header'); console.log(parse('<https://api.example.com/users?page=3>; rel=\"next\"'))"
```

## Header Format

```http
HTTP/1.1 200 OK
Link: <https://api.example.com/users?page=1>; rel="first",
      <https://api.example.com/users?page=3>; rel="next",
      <https://api.example.com/users?page=10>; rel="last"
```

## Testing
- Assert headers exist and URLs are absolute
- Verify last page omits rel=next
- Confirm empty results still emit valid links

## Best Practices
- Build links from request host, never hardcode
- Percent-encode query values in link URLs
- Combine with rel=prev for bidirectional navigation

## Capabilities

### link-headers
Expose pagination metadata in HTTP Link headers

**Commands:**
- `curl -sI 'http://localhost:8080/users?page=2&limit=10'`
- `curl -s -D- 'http://localhost:8080/users?page=2' | grep -i '^link:'`
- `npm install parse-link-header`
- `node -e "const parse=require('parse-link-header'); console.log(parse('demo-http-localhost-8080-users-page; rel=\"next\"'))"`
- `curl -s -o /dev/null -w '%{http_code}\n' 'http://localhost:8080/users?page=9999'`

**Examples:**
- Link: demo-page; rel="next" is the RFC 8288 wire format
- parse-link-header turns Link headers into a JS object
- grep -i '^link:' extracts pagination links from response headers

### header-validation
Validate Link header output against RFC 8288

**Commands:**
- `node -e "const h='demo-http-localhost-8080-users-page; rel=\"next\"'; const m=h.match(/demo-]+)>;\s*rel=\"(\w+)\"/); console.log(m ? m.slice(1) : 'invalid')"`
- `curl -s 'http://localhost:8080/users?page=1' -D- -o /dev/null | grep -ci 'link:'`
