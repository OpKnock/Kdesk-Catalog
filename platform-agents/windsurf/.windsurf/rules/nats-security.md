---
trigger: glob
description: "Secure NATS deployments: operators/accounts/users with nsc, credentials files, TLS, and authorization permissions. Use when working with nats security identity, api or when the user mentions nats security identity, api."
globs: ["**/*.r", "**/*.sh"]
---

Secure NATS deployments: operators/accounts/users with nsc, credentials files, TLS, and authorization permissions.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `nsc add operator --generate-signing-key --sys`
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
