# Curl

Tests and debugs REST APIs from the terminal with curl: methods, headers, JSON bodies, auth, TLS options, timing, and output formatting.

## Instructions

# curl

Test and debug APIs from the terminal with curl.

## When to Use

- Quick API smoke tests and debugging
- Reproducing reported issues with exact requests
- Verifying headers, auth, and TLS behavior

## Basic Requests

```bash
curl -i https://httpbin.org/get
curl -X POST -H "Content-Type: application/json" \
  -d '{"name":"alice"}' https://httpbin.org/post
curl -u alice:secret https://httpbin.org/basic-auth/alice/secret
curl -H "Authorization: Bearer $TOKEN" https://httpbin.org/bearer
```

## Inspecting Responses

```bash
curl -s -D headers.txt -o response.json https://httpbin.org/get
curl -w "status:%{http_code} time:%{time_total}s size:%{size_download}\n" \
  -o /dev/null https://httpbin.org/get
curl -v https://httpbin.org/get
```

## TLS and Debugging

```bash
curl -k https://httpbin.org/get
curl -k -v https://httpbin.org/get
curl --cacert ca.pem https://httpbin.org/get
```

## Data Files

```bash
curl -X POST -H "Content-Type: application/json" --data-binary @payload.json \
  https://httpbin.org/post
curl -F "file=@report.pdf" https://httpbin.org/post
```

## Testing

```bash
curl -o /dev/null -w "%{http_code}\n" https://httpbin.org/get
curl -s https://httpbin.org/get | jq '.origin'
```

## Best Practices

- Always set Content-Type for bodies
- Use -w for status codes and timing in scripts
- Never put credentials on the command line history; use env vars
- Use --data-binary for exact JSON payloads
- Add -f to fail fast on HTTP errors in scripts
- Read responses with jq for readability

## Capabilities

### requests
Send HTTP requests with curl covering methods, headers, bodies, and auth

**Commands:**
- `curl -i https://httpbin.org/get`
- `curl -X POST -H "Content-Type: application/json" -d '{"name":"alice"}' https://httpbin.org/post`
- `curl -u alice:secret https://httpbin.org/basic-auth/alice/secret`
- `curl -H "Authorization: Bearer $TOKEN" https://httpbin.org/bearer`

**Examples:**
- curl -X PUT -H "Content-Type: application/json" -d '{"name":"bob"}' https://httpbin.org/put
- curl -X DELETE -o /dev/null -w "%{http_code}\n" https://httpbin.org/delete
- curl -H "Accept: application/vnd.api+json" https://httpbin.org/get

### debugging
Inspect responses, headers, TLS, timing, and write output to files

**Commands:**
- `curl -s -D headers.txt -o response.json https://httpbin.org/get`
- `curl -k https://httpbin.org/get`
- `curl -w "status:%{http_code} time:%{time_total}s size:%{size_download}\n" -o /dev/null https://httpbin.org/get`
- `curl -v https://httpbin.org/get`

**Examples:**
- curl -w "%{time_connect} %{time_starttransfer} %{time_total}\n" -o /dev/null https://httpbin.org/get
- curl -k -v https://httpbin.org/get
- curl -s https://httpbin.org/get | jq '.origin'
