---
applyTo: "**/*.go **/*.r **/*.sh"
---

# Pulsar Security

Secure Pulsar: token authentication, namespace permissions, TLS encryption, and broker config.

## Instructions

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
