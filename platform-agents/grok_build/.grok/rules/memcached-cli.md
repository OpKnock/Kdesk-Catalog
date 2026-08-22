# memcached-cli

Operates memcached: server startup, key CRUD via telnet/netcat protocol, and stats.

## Instructions

# Memcached CLI

Distributed cache operations: run the server, read/write keys over the text
protocol, and pull stats.

## When to Use

- Debugging cache keys and TTLs
- Checking hit/miss rates and memory usage
- Flushing caches during development

## Real Commands

```bash
# Start a server (64MB, daemonized)
sudo memcached -p 11211 -u memcached -m 64 -d

# Set a key: set <key> <flags> <ttl> <bytes>
printf 'set user:42 0 300 5\r\nhello\r\n' | nc localhost 11211

# Get
printf 'get user:42\r\n' | nc localhost 11211

# Delete
printf 'delete user:42\r\n' | nc localhost 11211

# Stats
printf 'stats\r\n' | nc -q1 localhost 11211

# Use memcached-tool instead
sudo memcached-tool 127.0.0.1:11211 stats

# Flush (dev only!)
printf 'flush_all\r\n' | nc localhost 11211
```

## Key Stats

- `get_hits` / `get_misses` - hit ratio
- `curr_items`, `evictions` - capacity pressure
- `bytes` vs `limit_maxbytes` - memory usage

## Best Practices

- Set realistic TTLs; 30 days max key TTL
- Prefer CAS (`gets`/`cas`) for read-modify-write
- Watch evictions; that means cache too small or TTLs too long
- Never store sensitive data; it's unencrypted by default
- Use binary protocol in apps (libmemcached) for speed

## Example Response

Sets/gets test keys, then reports hit ratio, evictions, and memory usage from
stats to evaluate cache effectiveness.

## Capabilities

### memcached-protocol
Set/get/delete keys and inspect stats via the memcached text protocol

**Commands:**
- `memcached -p 11211 -u memcached -m 64`
- `printf 'set mykey 0 60 5\r\nhello\r\n' | nc localhost 11211`
- `printf 'get mykey\r\n' | nc localhost 11211`
- `printf 'stats\r\n' | nc -q1 localhost 11211`
- `printf 'delete mykey\r\n' | nc localhost 11211`

**Examples:**
- printf 'set session:abc 0 1800 11\r\nvalue=12345\r\n' | nc localhost 11211
- memcached-tool 127.0.0.1:11211 stats
- printf 'flush_all\r\n' | nc localhost 11211