Implements RFC 8288 Link headers for pagination: rel=next/prev/first/last, parsing with standard libraries, and REST hypermedia navigation.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -sI 'http://localhost:8080/users?page=2&limit=10'`, `node -e "const h='demo-http-localhost-8080-users-page; rel=\`
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

**Parameters:**
- `rel` (string): Link relation: next, prev, first, last
- `page` (integer): Current page number for URL construction
- `limit` (integer): Items per page reflected in link URLs

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

**Examples:**
- -cli --help
- -api --help

## References
- [RFC 8288 - Web Linking](https://www.rfc-editor.org/rfc/rfc8288)
- [parse-link-header](https://github.com/remy/parse-link-header)