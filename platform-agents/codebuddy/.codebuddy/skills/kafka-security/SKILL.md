---
name: "kafka-security"
description: "Secure Kafka: SCRAM-SHA-256 credentials, ACLs for topics/groups/clusters, TLS client configs, and verifying authorized access."
---

# Kafka Security

Secure Kafka: SCRAM-SHA-256 credentials, ACLs for topics/groups/clusters, TLS client configs, and verifying authorized access.

## Instructions

# Kafka Security

Lock down Kafka with SASL authentication, TLS encryption, and ACL authorization.

## What this skill does

- Creates SCRAM-SHA-256/512 credentials for clients.
- Grants and revokes fine-grained ACLs (topic, group, cluster).
- Writes client properties for SASL_SSL connections.

## When to use

- Enforcing multi-tenant access control on shared clusters.
- Compliance audits that require principal-level accounting.
- Securing replication and tooling connections.

## Real commands

```bash
# Create SCRAM user
kafka-configs.sh --bootstrap-server localhost:9092 \
  --entity-type users --entity-name alice --alter \
  --add-config "SCRAM-SHA-256=[iterations=8192,password=secret]"

# Grant topic read/write
kafka-acls.sh --bootstrap-server localhost:9092 \
  --add --allow-principal User:alice \
  --operation Read --operation Write --topic orders

# Grant group read (required for consuming)
kafka-acls.sh --bootstrap-server localhost:9092 \
  --add --allow-principal User:alice --group analytics --operation Read

# Cluster admin ACL
kafka-acls.sh --bootstrap-server localhost:9092 \
  --add --allow-principal User:admin --cluster --operation Alter

# List ACLs for a topic
kafka-acls.sh --bootstrap-server localhost:9092 --list --topic orders

# Revoke
kafka-acls.sh --bootstrap-server localhost:9092 \
  --remove --allow-principal User:alice --operation Write --topic orders
```

## Client properties (SASL_SSL)

```properties
security.protocol=SASL_SSL
sasl.mechanism=SCRAM-SHA-256
sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required username="alice" password="secret";
ssl.truststore.location=/etc/kafka/truststore.jks
```

## Testing

```bash
# Verify access
kafka-console-consumer.sh --bootstrap-server localhost:9092 \
  --topic orders --group analytics --consumer.config client.properties --max-messages 1
```

## Best practices

- Grant group ACLs alongside topic ACLs or consumption fails with GroupAuthorizationException.
- Use prefixes for wildcard ACLs sparingly; explicit beats wildcard.
- Rotate SCRAM credentials and keep JAAS passwords out of git.

## Capabilities

### authn
Manage SCRAM users and SASL credentials for clients.

**Commands:**
- `kafka-configs.sh --bootstrap-server localhost:9092 --entity-type users --entity-name alice --alter --add-config "SCRAM-SHA-256=[iterations=8192,password=secret]"`
- `kafka-configs.sh --bootstrap-server localhost:9092 --entity-type users --entity-name alice --alter --add-config "SCRAM-SHA-512=[iterations=8192,password=secret]"`
- `kafka-configs.sh --bootstrap-server localhost:9092 --entity-type users --entity-name alice --describe`
- `kafka-configs.sh --bootstrap-server localhost:9092 --entity-type users --entity-name alice --alter --delete-config 'SCRAM-SHA-256'`

**Examples:**
- kafka-configs.sh --bootstrap-server localhost:9092 --entity-type users --entity-name alice --alter --add-config "SCRAM-SHA-256=[iterations=8192,password=secret]"
- kafka-configs.sh --bootstrap-server localhost:9092 --entity-type users --entity-name alice --describe

### authorization
Grant and revoke ACLs on topics, consumer groups, and cluster operations.

**Commands:**
- `kafka-acls.sh --bootstrap-server localhost:9092 --add --allow-principal User:alice --operation Read --operation Write --topic orders`
- `kafka-acls.sh --bootstrap-server localhost:9092 --add --allow-principal User:alice --group analytics --operation Read`
- `kafka-acls.sh --bootstrap-server localhost:9092 --add --allow-principal User:admin --cluster --operation Alter`
- `kafka-acls.sh --bootstrap-server localhost:9092 --list --topic orders`
- `kafka-acls.sh --bootstrap-server localhost:9092 --remove --allow-principal User:alice --operation Write --topic orders`

**Examples:**
- kafka-acls.sh --bootstrap-server localhost:9092 --add --allow-principal User:alice --operation Read --operation Write --topic orders
- kafka-acls.sh --bootstrap-server localhost:9092 --list --topic orders
- kafka-acls.sh --bootstrap-server localhost:9092 --remove --allow-principal User:alice --operation Write --topic orders
