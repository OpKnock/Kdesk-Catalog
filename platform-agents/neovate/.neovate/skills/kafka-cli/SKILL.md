---
name: "kafka-cli"
description: "Kafka CLI commands. Real kafka CLI."
---

# kafka-cli

Kafka CLI commands. Real kafka CLI.

## Instructions

# Kafka CLI

Kafka CLI commands using real CLI.

## When to Use

- Kafka operations
- Message streaming
- Topic management

## Commands

```bash
# Install
brew install kafka  # macOS

# Create topic
kafka-topics --create --topic mytopic --partitions 3 --replication-factor 1 --bootstrap-server localhost:9092

# List topics
kafka-topics --list --bootstrap-server localhost:9092

# Describe topic
kafka-topics --describe --topic mytopic --bootstrap-server localhost:9092

# Delete topic
kafka-topics --delete --topic mytopic --bootstrap-server localhost:9092

# Produce
kafka-console-producer --topic mytopic --bootstrap-server localhost:9092

# Consume
kafka-console-consumer --topic mytopic --from-beginning --bootstrap-server localhost:9092

# Consumer groups
kafka-consumer-groups --list --bootstrap-server localhost:9092

# Describe group
kafka-consumer-groups --describe --group mygroup --bootstrap-server localhost:9092
```

## Topic Operations

```bash
# Create topic
kafka-topics --create --topic mytopic --partitions 3 --replication-factor 1 --bootstrap-server localhost:9092

# List topics
kafka-topics --list --bootstrap-server localhost:9092

# Describe topic
kafka-topics --describe --topic mytopic --bootstrap-server localhost:9092

# Delete topic
kafka-topics --delete --topic mytopic --bootstrap-server localhost:9092

# Alter topic
kafka-topics --alter --topic mytopic --partitions 6 --bootstrap-server localhost:9092

# Config
kafka-topics --alter --topic mytopic --config retention.ms=86400000 --bootstrap-server localhost:9092
```

## Producer

```bash
# Produce
kafka-console-producer --topic mytopic --bootstrap-server localhost:9092

# Produce with key
kafka-console-producer --topic mytopic --property parse.key=true --property key.separator=: --bootstrap-server localhost:9092

# Produce from file
kafka-console-producer --topic mytopic --bootstrap-server localhost:9092 < messages.txt
```

## Consumer

```bash
# Consume
kafka-console-consumer --topic mytopic --from-beginning --bootstrap-server localhost:9092

# Consume with key
kafka-console-consumer --topic mytopic --property print.key=true --property key.separator=: --from-beginning --bootstrap-server localhost:9092

# Consume with group
kafka-console-consumer --topic mytopic --group mygroup --from-beginning --bootstrap-server localhost:9092

# Consume with max messages
kafka-console-consumer --topic mytopic --max-messages 10 --bootstrap-server localhost:9092
```

## Consumer Groups

```bash
# List groups
kafka-consumer-groups --list --bootstrap-server localhost:9092

# Describe group
kafka-consumer-groups --describe --group mygroup --bootstrap-server localhost:9092

# Reset offset
kafka-consumer-groups --group mygroup --topic mytopic --reset-offsets --to-earliest --execute --bootstrap-server localhost:9092

# Delete group
kafka-consumer-groups --delete --group mygroup --bootstrap-server localhost:9092
```

## Examples

```bash
# Create topic
kafka-topics --create --topic mytopic --partitions 3 --replication-factor 1 --bootstrap-server localhost:9092

# Produce
kafka-console-producer --topic mytopic --bootstrap-server localhost:9092

# Consume
kafka-console-consumer --topic mytopic --from-beginning --bootstrap-server localhost:9092
```

## CI/CD

```yaml
# GitHub Actions
- name: Kafka CLI
  run: |
    kafka-topics --list --bootstrap-server localhost:9092

# GitLab CI
kafka:
  stage: test
  script:
    - kafka-topics --list --bootstrap-server localhost:9092
```

## Capabilities

### kafka-cli
Kafka CLI commands. Real kafka CLI.

**Commands:**
- `brew install kafka`
- `kafka-topics --create --topic mytopic --partitions 3 --replication-factor 1 --bootstrap-server localhost:9092`
- `kafka-topics --list --bootstrap-server localhost:9092`
- `kafka-topics --describe --topic mytopic --bootstrap-server localhost:9092`
- `kafka-topics --delete --topic mytopic --bootstrap-server localhost:9092`
- `kafka-console-producer --topic mytopic --bootstrap-server localhost:9092`
- `kafka-console-consumer --topic mytopic --from-beginning --bootstrap-server localhost:9092`
- `kafka-consumer-groups --list --bootstrap-server localhost:9092`
- `kafka-consumer-groups --describe --group mygroup --bootstrap-server localhost:9092`
- `kafka-topics --create --topic mytopic --partitions 3 --replication-factor 1 --bootstrap-server localhost:9092`
- `kafka-topics --list --bootstrap-server localhost:9092`
- `kafka-topics --describe --topic mytopic --bootstrap-server localhost:9092`
- `kafka-topics --delete --topic mytopic --bootstrap-server localhost:9092`
- `kafka-topics --alter --topic mytopic --partitions 6 --bootstrap-server localhost:9092`
- `kafka-topics --alter --topic mytopic --config retention.ms=86400000 --bootstrap-server localhost:9092`
- `kafka-console-producer --topic mytopic --bootstrap-server localhost:9092`
- `kafka-console-producer --topic mytopic --property parse.key=true --property key.separator=: --bootstrap-server localhost:9092`
- `kafka-console-producer --topic mytopic --bootstrap-server localhost:9092 < messages.txt`
- `kafka-console-consumer --topic mytopic --from-beginning --bootstrap-server localhost:9092`
- `kafka-console-consumer --topic mytopic --property print.key=true --property key.separator=: --from-beginning --bootstrap-server localhost:9092`
- `kafka-console-consumer --topic mytopic --group mygroup --from-beginning --bootstrap-server localhost:9092`
- `kafka-console-consumer --topic mytopic --max-messages 10 --bootstrap-server localhost:9092`
- `kafka-consumer-groups --list --bootstrap-server localhost:9092`
- `kafka-consumer-groups --describe --group mygroup --bootstrap-server localhost:9092`
- `kafka-consumer-groups --group mygroup --topic mytopic --reset-offsets --to-earliest --execute --bootstrap-server localhost:9092`
- `kafka-consumer-groups --delete --group mygroup --bootstrap-server localhost:9092`
- `kafka-topics --create --topic mytopic --partitions 3 --replication-factor 1 --bootstrap-server localhost:9092`
- `kafka-console-producer --topic mytopic --bootstrap-server localhost:9092`
- `kafka-console-consumer --topic mytopic --from-beginning --bootstrap-server localhost:9092`

**Examples:**
- brew install kafka
- kafka-topics --create --topic mytopic --partitions 3 --replication-factor 1 --bootstrap-server localhost:9092
- kafka-topics --list --bootstrap-server localhost:9092
