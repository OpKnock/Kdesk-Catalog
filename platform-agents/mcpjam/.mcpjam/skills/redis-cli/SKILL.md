---
name: "redis-cli"
description: "Redis CLI commands. Real redis-cli CLI."
---

# redis-cli

Redis CLI commands. Real redis-cli CLI.

## Instructions

# Redis CLI

Redis CLI commands using real CLI.

## When to Use

- Redis operations
- Cache management
- Key-value store

## Commands

```bash
# Install
brew install redis  # macOS

# Connect
redis-cli

# Connect with host
redis-cli -h localhost -p 6379

# Connect with password
redis-cli -a password

# Connect with TLS
redis-cli --tls

# Ping
redis-cli ping

# Set key
redis-cli SET key value

# Get key
redis-cli GET key

# Delete key
redis-cli DEL key

# Exists
redis-cli EXISTS key

# Expire
redis-cli EXPIRE key 60

# TTL
redis-cli TTL key

# Type
redis-cli TYPE key

# Keys
redis-cli KEYS pattern*

# Info
redis-cli INFO

# Config get
redis-cli CONFIG GET maxmemory

# Config set
redis-cli CONFIG SET maxmemory 256mb
```

## String Operations

```bash
# Set
redis-cli SET key value

# Get
redis-cli GET key

# Set with expiry
redis-cli SETEX key 60 value

# Set if not exists
redis-cli SETNX key value

# Get set
redis-cli GETSET key newvalue

# Increment
redis-cli INCR key

# Decrement
redis-cli DECR key

# Increment by
redis-cli INCRBY key 5

# Append
redis-cli APPEND key value

# Strlen
redis-cli STRLEN key
```

## List Operations

```bash
# Push left
redis-cli LPUSH key value

# Push right
redis-cli RPUSH key value

# Pop left
redis-cli LPOP key

# Pop right
redis-cli RPOP key

# Range
redis-cli LRANGE key 0 -1

# Length
redis-cli LLEN key

# Index
redis-cli LINDEX key 0

# Set
redis-cli LSET key 0 value

# Trim
redis-cli LTRIM key 0 9
```

## Hash Operations

```bash
# Set field
redis-cli HSET key field value

# Get field
redis-cli HGET key field

# Get all
redis-cli HGETALL key

# Delete field
redis-cli HDEL key field

# Exists field
redis-cli HEXISTS key field

# Length
redis-cli HLEN key

# Keys
redis-cli HKEYS key

# Values
redis-cli HVALS key
```

## Set Operations

```bash
# Add
redis-cli SADD key member

# Remove
redis-cli SREM key member

# Members
redis-cli SMEMBERS key

# Is member
redis-cli SISMEMBER key member

# Union
redis-cli SUNION key1 key2

# Intersection
redis-cli SINTER key1 key2

# Difference
redis-cli SDIFF key1 key2

# Random member
redis-cli SRANDMEMBER key

# Pop
redis-cli SPOP key
```

## Sorted Set Operations

```bash
# Add
redis-cli ZADD key score member

# Range
redis-cli ZRANGE key 0 -1 WITHSCORES

# Range by score
redis-cli ZRANGEBYSCORE key 0 100

# Remove
redis-cli ZREM key member

# Score
redis-cli ZSCORE key member

# Rank
redis-cli ZRANK key member

# Count
redis-cli ZCARD key

# Count by score
redis-cli ZCOUNT key 0 100
```

## Pub/Sub

```bash
# Subscribe
redis-cli SUBSCRIBE channel

# Publish
redis-cli PUBLISH channel message

# PSUBSCRIBE
redis-cli PSUBSCRIBE pattern*
```

## Transactions

```bash
# Watch
redis-cli WATCH key

# Multi
redis-cli MULTI

# Exec
redis-cli EXEC

# Discard
redis-cli DISCARD
```

## Examples

```bash
# Connect
redis-cli

# Set/Get
redis-cli SET key value
redis-cli GET key

# Keys
redis-cli KEYS *

# Info
redis-cli INFO
```

## CI/CD

```yaml
# GitHub Actions
- name: Redis CLI
  run: |
    redis-cli ping

# GitLab CI
redis:
  stage: test
  script:
    - redis-cli ping
```

## Capabilities

### redis-cli
Redis CLI commands. Real redis-cli CLI.

**Commands:**
- `brew install redis`
- `redis-cli`
- `redis-cli -h localhost -p 6379`
- `redis-cli -a password`
- `redis-cli --tls`
- `redis-cli ping`
- `redis-cli SET key value`
- `redis-cli GET key`
- `redis-cli DEL key`
- `redis-cli EXISTS key`
- `redis-cli EXPIRE key 60`
- `redis-cli TTL key`
- `redis-cli TYPE key`
- `redis-cli KEYS pattern*`
- `redis-cli INFO`
- `redis-cli CONFIG GET maxmemory`
- `redis-cli CONFIG SET maxmemory 256mb`
- `redis-cli SET key value`
- `redis-cli GET key`
- `redis-cli SETEX key 60 value`
- `redis-cli SETNX key value`
- `redis-cli GETSET key newvalue`
- `redis-cli INCR key`
- `redis-cli DECR key`
- `redis-cli INCRBY key 5`
- `redis-cli APPEND key value`
- `redis-cli STRLEN key`
- `redis-cli LPUSH key value`
- `redis-cli RPUSH key value`
- `redis-cli LPOP key`
- `redis-cli RPOP key`
- `redis-cli LRANGE key 0 -1`
- `redis-cli LLEN key`
- `redis-cli LINDEX key 0`
- `redis-cli LSET key 0 value`
- `redis-cli LTRIM key 0 9`
- `redis-cli HSET key field value`
- `redis-cli HGET key field`
- `redis-cli HGETALL key`
- `redis-cli HDEL key field`
- `redis-cli HEXISTS key field`
- `redis-cli HLEN key`
- `redis-cli HKEYS key`
- `redis-cli HVALS key`
- `redis-cli SADD key member`
- `redis-cli SREM key member`
- `redis-cli SMEMBERS key`
- `redis-cli SISMEMBER key member`
- `redis-cli SUNION key1 key2`
- `redis-cli SINTER key1 key2`
- `redis-cli SDIFF key1 key2`
- `redis-cli SRANDMEMBER key`
- `redis-cli SPOP key`
- `redis-cli ZADD key score member`
- `redis-cli ZRANGE key 0 -1 WITHSCORES`
- `redis-cli ZRANGEBYSCORE key 0 100`
- `redis-cli ZREM key member`
- `redis-cli ZSCORE key member`
- `redis-cli ZRANK key member`
- `redis-cli ZCARD key`
- `redis-cli ZCOUNT key 0 100`
- `redis-cli SUBSCRIBE channel`
- `redis-cli PUBLISH channel message`
- `redis-cli PSUBSCRIBE pattern*`
- `redis-cli WATCH key`
- `redis-cli MULTI`
- `redis-cli EXEC`
- `redis-cli DISCARD`
- `redis-cli`
- `redis-cli SET key value`
- `redis-cli GET key`
- `redis-cli KEYS *`
- `redis-cli INFO`

**Examples:**
- brew install redis
- redis-cli
- redis-cli -h localhost -p 6379
