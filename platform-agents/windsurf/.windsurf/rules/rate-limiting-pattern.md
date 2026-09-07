---
trigger: glob
description: "Rate limiting architecture patterns: edge vs service-level, distributed limits with Redis, and Envoy filter setup. Use when working with rate limit patterns, api or when the user mentions rate limit patterns, api."
globs: ["**/*.go", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

Rate limiting architecture patterns: edge vs service-level, distributed limits with Redis, and Envoy filter setup.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `envoy --config-path envoy.yaml`
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

# Rate Limiting Patterns

Rate limits live at different layers: reverse proxy, gateway, or application.

## What this skill does

- Builds distributed limits with Redis sorted sets
- Configures Envoy rate limit filters
- Chooses the right layer per use case

## When to use

- Multi-instance apps need shared limits
- Offloading limits to the edge

## Real commands

```bash
# Envoy
envoy --config-path envoy.yaml

# Redis sliding window
redis-cli ZREMRANGEBYSCORE user:42:rl 0 $(date +%s000 -d '-60 seconds')
redis-cli ZADD user:42:rl $(date +%s000) $(date +%s000)
redis-cli ZCARD user:42:rl

# Verify
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:10000/api
```

## Envoy filter

```yaml
http_filters:
- name: envoy.filters.http.local_ratelimit
  typed_config:
    "@type": type.googleapis.com/envoy.extensions.filters.http.local_ratelimit.v3.LocalRateLimit
    stat_prefix: http_local_rate_limiter
    token_bucket:
      max_tokens: 100
      tokens_per_fill: 10
      fill_interval: 1s
    status:
      code: TooManyRequests
```

## Pattern guidance

- Edge limits protect the whole fleet
- App-level limits enable business quotas
- Use Redis when instances are stateless

## Best practices

- Combine edge and service-level limits
- Use ZSETs with timestamps for sliding windows
- Return 429 + Retry-After consistently

## Capabilities

### rate-limit-patterns
Implement distributed rate limiting patterns with Redis sliding window and Envoy rate limit filters.

**Parameters:**
- `key` (string): Redis sorted set key for the window
- `window_seconds` (integer): Sliding window size
- `limit` (integer): Max requests per window

**Commands:**
- `envoy --config-path envoy.yaml`
- `redis-cli ZREMRANGEBYSCORE user:42:rl 0 $(date +%s000 -d '-60 seconds')`
- `redis-cli ZADD user:42:rl $(date +%s000) $(date +%s000)`
- `redis-cli ZCARD user:42:rl`
- `curl -s -o /dev/null -w "%{http_code}\n" http://localhost:10000/api`

**Examples:**
- redis-cli ZADD user:42:rl 1710000000000 1710000000000; redis-cli ZCARD user:42:rl
- curl -s -o /dev/null -w "%{http_code}\n" http://localhost:10000/api
- redis-cli ZREMRANGEBYSCORE user:42:rl 0 1710000000000

## References
- [Envoy Rate Limit Filter](https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/rate_limit_filter)
- [Redis sliding window pattern](https://redis.io/glossary/rate-limiting/)
