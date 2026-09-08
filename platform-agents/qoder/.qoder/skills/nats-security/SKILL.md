---
name: "nats-security"
description: "Secure NATS deployments: operators/accounts/users with nsc, credentials files, TLS, and authorization permissions. Use when working with nats security identity, api or when the user mentions nats security identity, api."
license: "MIT"
compatibility: "Requires nats, nsc."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(nats:*) Bash(nsc:*)"
---

Secure NATS deployments: operators/accounts/users with nsc, credentials files, TLS, and authorization permissions.

## Agentic Workflow: Read -> Reason -> Act (nats-security)

You are **Nats Security** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `nats-security`
- Domain: Secure NATS deployments: operators/accounts/users with nsc, credentials files, TLS, and authorization permissions.
- **nats-security-identity**: Create NATS operator/account/user hierarchies with nsc and connect using credentials files. — `nsc add operator --generate-signing-key --sys`
- Check `knowledge` and `prerequisites: nats, nsc`

### 2. Reason — think for `nats-security`
- For `nats-security-identity`: Create NATS operator/account/user hierarchies with nsc and connect using credentials files. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `nats-security` tools
- Tools: `Glob`, `Grep`, `Read`, `Nsc`, `Nats` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `nats-security:ee9d2478`

# NATS Security

NATS uses JWT-based identity: an operator owns accounts, accounts contain users, users hold credentials.

## What this skill does

- Bootstraps the nsc operator/account/user hierarchy
- Grants pub/sub permissions per user
- Connects clients with .creds files and nats context

## When to use

- Multi-tenant NATS deployments
- Enforcing least-privilege per service
- TLS-encrypted NATS traffic

## Real commands

```bash
# Operator and account
nsc add operator --generate-signing-key --sys
nsc add account prod

# User with permissions
nsc add user api --allow-pub 'orders.*' --allow-sub 'orders.>'

# Export creds and create a context
nsc describe user api
nats context save prod --server nats://localhost:4222 --creds ~/.nsc/creds/prod/api/user.creds

# Use it
nats --creds user.creds pub orders.created '{"id":1}'
```

## Server config with JWT

```conf
operator: /etc/nats/op.jwt
system_account: SYS
resolver: {
  type: full
  dir: /var/lib/nats/jwt
}
```

## Best practices

- Never share operator keys; keep them offline
- Grant narrow subject permissions per service
- Rotate user credentials by creating new users in nsc

## Capabilities

### nats-security-identity
Create NATS operator/account/user hierarchies with nsc and connect using credentials files.

**Parameters:**
- `operator` (string): Operator name
- `account` (string): Account name the user belongs to
- `permissions` (array): Pub/sub allow-deny rules for the user

**Commands:**
- `nsc add operator --generate-signing-key --sys`
- `nsc add account prod`
- `nsc add user api --allow-pub 'orders.*' --allow-sub 'orders.>'`
- `nats context save --server nats://localhost:4222 --creds ~/.nsc/creds/prod/api/user.creds prod`
- `nsc list accounts`

**Examples:**
- nsc edit user api --allow-pub-sub 'orders.*'
- nsc add user svc --allow-pub 'reply.*' --allow-sub 'req.*'
- nats --creds user.creds pub orders.created '{"id":1}'

## References
- [NATS Security Docs](https://docs.nats.io/running-a-nats-service/configuration/securing_nats)
- [NATS CLI Security Tutorial](https://docs.nats.io/running-a-nats-service/nats_admin/security)
