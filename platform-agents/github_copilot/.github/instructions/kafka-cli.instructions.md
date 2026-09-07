---
applyTo: "**/*.r **/*.sh **/*.{yaml,yml}"
---

Kafka CLI commands. Real kafka CLI.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `brew install kafka`
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

**Parameters:**
- `alter` (boolean): CLI flag --alter observed in capability commands
- `bootstrap-server` (string): CLI flag --bootstrap-server observed in capability commands
- `create` (boolean): CLI flag --create observed in capability commands
- `delete` (boolean): CLI flag --delete observed in capability commands
- `describe` (boolean): CLI flag --describe observed in capability commands
- `from-beginning` (boolean): CLI flag --from-beginning observed in capability commands
- `group` (string): CLI flag --group observed in capability commands
- `list` (boolean): CLI flag --list observed in capability commands
- `partitions` (number): CLI flag --partitions observed in capability commands
- `property` (string): CLI flag --property observed in capability commands
- `replication-factor` (number): CLI flag --replication-factor observed in capability commands
- `topic` (string): CLI flag --topic observed in capability commands

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

## References
- [kafka-cli Skill Documentation](skills/database/kafka-cli.md)
