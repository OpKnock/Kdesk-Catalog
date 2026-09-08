---
trigger: glob
description: "Secure Pulsar: token authentication, namespace permissions, TLS encryption, and broker config. Use when working with pulsar security hardening, api or when the user mentions pulsar security hardening, api."
globs: ["**/*.go", "**/*.r", "**/*.sh"]
---

Secure Pulsar: token authentication, namespace permissions, TLS encryption, and broker config.

## Agentic Workflow: Read -> Reason -> Act (pulsar-security)

You are **Pulsar Security** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `pulsar-security`
- Domain: Secure Pulsar: token authentication, namespace permissions, TLS encryption, and broker config.
- **pulsar-security-hardening**: Configure token auth, TLS, and role-based namespace permissions with pulsar-admin. — `bin/pulsar tokens create --secret-key my-secret.key --subject admin`
- Check `knowledge` and `prerequisites: bin/pulsar, bin/pulsar-admin`

### 2. Reason — think for `pulsar-security`
- For `pulsar-security-hardening`: Configure token auth, TLS, and role-based namespace permissions with pulsar-admin. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `pulsar-security` tools
- Tools: `Glob`, `Grep`, `Read`, `Bin/pulsar`, `Bin/pulsar-admin` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `pulsar-security:70d273c5`

# Pulsar Security

Lock down Pulsar with tokens, roles and TLS so only authorized clients touch topics.

## What this skill does

- Generates JWT tokens per service
- Grants/revokes namespace permissions
- Configures TLS endpoints

## When to use

- Production cluster rollout
- Restricting topic access per team

## Real commands

```bash
# Token for a role
bin/pulsar tokens create --secret-key my-secret.key --subject admin
bin/pulsar tokens create --secret-key my-secret.key --subject svc-orders

# Enable auth
bin/pulsar-admin brokers update-dynamic-config --config authenticationEnabled --value true

# Permissions
bin/pulsar-admin namespaces grant-permission --role svc-orders \
  --actions produce,consume public/default/orders-topic
bin/pulsar-admin namespaces revoke-permission --role svc-orders public/default/orders-topic
bin/pulsar-admin namespaces permissions public/default
```

## Client with token

```go
pulsar.ClientOptions{URL: "pulsar+ssl://localhost:6651", Authentication: pulsar.NewAuthenticationToken(token)}
```

## broker.conf security

```conf
authenticationEnabled=true
authenticationProviders=org.apache.pulsar.broker.authentication.AuthenticationProviderToken
tlsEnabled=true
tlsCertificateFilePath=/etc/pulsar/server.crt
tlsKeyFilePath=/etc/pulsar/server.key
```

## Best practices

- One token per service, one role per service
- Rotate tokens on a schedule
- Use pulsar+ssl:// and client certs for TLS

## Capabilities

### pulsar-security-hardening
Configure token auth, TLS, and role-based namespace permissions with pulsar-admin.

**Parameters:**
- `role` (string): Subject/role the token or permission is for
- `actions` (string): produce, consume, or functions
- `namespace` (string): Target namespace

**Commands:**
- `bin/pulsar tokens create --secret-key my-secret.key --subject admin`
- `bin/pulsar-admin brokers update-dynamic-config --config authenticationEnabled --value true`
- `bin/pulsar-admin namespaces grant-permission --role svc-orders --actions produce,consume public/default/orders-topic`
- `bin/pulsar-admin namespaces revoke-permission --role svc-orders public/default/orders-topic`
- `bin/pulsar-admin namespaces permissions public/default`

**Examples:**
- bin/pulsar tokens create --secret-key my-secret.key --subject svc-orders | tee svc-orders.token
- bin/pulsar-admin namespaces grant-permission --role admin --actions produce,consume public/default
- bin/pulsar-admin namespaces permissions public/default | jq .

## References
- [Pulsar Security Overview](https://pulsar.apache.org/docs/3.0.x/security-overview/)
- [Token Auth](https://pulsar.apache.org/docs/3.0.x/security-token-auth/)
