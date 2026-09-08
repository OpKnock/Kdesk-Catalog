---
trigger: glob
description: "Lock down Redis with ACL users, password auth, TLS listeners, and renamed dangerous commands to meet production hardening requirements. Use when working with redis hardening, api or when the user mentions redis hardening, api."
globs: ["**/*.r", "**/*.sh"]
---

Lock down Redis with ACL users, password auth, TLS listeners, and renamed dangerous commands to meet production hardening requirements.

## Agentic Workflow: Read -> Reason -> Act (redis-security)

You are **Redis Security** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `redis-security`
- Domain: Lock down Redis with ACL users, password auth, TLS listeners, and renamed dangerous commands to meet production hardening requirements.
- **redis-hardening**: Lock down Redis with ACLs, passwords, TLS, and command renaming — `redis-cli ACL LIST`
- Check `knowledge` and `prerequisites: redis-cli`

### 2. Reason — think for `redis-security`
- For `redis-hardening`: Lock down Redis with ACLs, passwords, TLS, and command renaming — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `redis-security` tools
- Tools: `Glob`, `Grep`, `Read`, `Redis-cli` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `redis-security:14680a18`

# Redis Security

Hand-crafted skill for hardening Redis instances against exposure and misuse.

## What this skill does

- Creates least-privilege ACL users with key and command allowlists
- Enables requirepass for the default user and rewrites the config
- Configures a TLS listener and renames dangerous commands like FLUSHALL

## When to use

- A Redis instance is reachable from outside localhost
- Multiple teams share one server and need isolated permissions
- Compliance reviews ask for auth on all datastores

## Real commands

```bash
# Inventory users
redis-cli ACL LIST

# Create a scoped app user
redis-cli ACL SETUSER appuser on >StrongPass123 ~cache:* +get +set +del

# Inspect a user's effective rules
redis-cli --no-auth-warning -a 'pass' ACL GETUSER appuser

# Password-protect the default user
redis-cli CONFIG SET requirepass 's3cr3t'
redis-cli CONFIG REWRITE

# TLS listener check
redis-cli -p 6380 --tls --cacert /etc/redis/ca.crt PING
```

## Config example

```conf
# redis.conf
bind 127.0.0.1 10.0.0.5
protected-mode yes
requirepass s3cr3t
rename-command FLUSHALL ""

port 6379
port 6380 tls
tls-port 6380
tls-cert-file /etc/redis/server.crt
tls-key-file /etc/redis/server.key
tls-ca-cert-file /etc/redis/ca.crt
```

## Testing

```bash
redis-cli -a 's3cr3t' ping
redis-cli -p 6380 --tls --cacert ca.crt -a 's3cr3t' ping
redis-cli ACL WHOAMI
```

## Best practices

- Never bind 0.0.0.0 without TLS plus a strong password
- Give each service its own ACL user with only the commands it needs
- Rename FLUSHALL/FLUSHDB/KEYS on shared servers

## Capabilities

### redis-hardening
Lock down Redis with ACLs, passwords, TLS, and command renaming

**Parameters:**
- `username` (string): ACL user to create or modify
- `key_pattern` (string): Key pattern the user may touch, e.g. cache:*
- `commands` (string): Allow/deny command list, e.g. +get -set

**Commands:**
- `redis-cli ACL LIST`
- `redis-cli ACL SETUSER appuser on >StrongPass123 ~cache:* +get +set +del`
- `redis-cli --no-auth-warning -a 'pass' ACL GETUSER appuser`
- `redis-cli CONFIG SET requirepass 's3cr3t'`
- `redis-cli CONFIG REWRITE`
- `redis-cli -p 6380 --tls --cacert /etc/redis/ca.crt PING`

**Examples:**
- redis-cli ACL SETUSER readonly on >pw123 ~cache:* +get -set
- redis-cli CONFIG GET bind
- redis-cli --tls --cacert ca.crt -a $REDIS_PASS ping

## References
- [Redis Security](https://redis.io/docs/latest/operate/oss_and_stack/management/security/)
- [ACL command reference](https://redis.io/docs/latest/commands/acl-setuser/)
