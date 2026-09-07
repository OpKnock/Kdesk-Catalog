---
trigger: glob
description: "Secure Kafka: SCRAM-SHA-256 credentials, ACLs for topics/groups/clusters, TLS client configs, and verifying authorized access. Use when working with authn, authorization, api or when the user mentions authn, authorization, api."
globs: ["**/*.r", "**/*.rs", "**/*.sh"]
---

Secure Kafka: SCRAM-SHA-256 credentials, ACLs for topics/groups/clusters, TLS client configs, and verifying authorized access.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `kafka-configs.sh --bootstrap-server localhost:9092 --entity-`, `kafka-acls.sh --bootstrap-server localhost:9092 --add --allo`
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

**Parameters:**
- `user` (string): Principal user name.
- `mechanism` (string): SCRAM-SHA-256 or SCRAM-SHA-512.

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

**Parameters:**
- `principal` (string): User:<name> principal.
- `operation` (string): Read, Write, Describe, Alter, Create, Delete.
- `resource` (string): Topic, group, or --cluster resource.

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

## References
- [Kafka Security](https://kafka.apache.org/documentation/#security)
- [kafka-acls.sh](https://kafka.apache.org/documentation/#security_authz_cli)
