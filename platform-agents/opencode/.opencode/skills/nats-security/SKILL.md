---
name: "nats-security"
description: "Secure NATS deployments: operators/accounts/users with nsc, credentials files, TLS, and authorization permissions."
---

# Nats Security

Secure NATS deployments: operators/accounts/users with nsc, credentials files, TLS, and authorization permissions.

## Instructions

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
