---
trigger: glob
description: "RabbitMQ clients in Java with amqp-client: ConnectionFactory, publishes, consumers, and RPC patterns. Use when working with rabbitmq java client, api or when the user mentions rabbitmq java client, api."
globs: ["**/*.java", "**/*.r", "**/*.sh"]
---

RabbitMQ clients in Java with amqp-client: ConnectionFactory, publishes, consumers, and RPC patterns.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `mvn dependency:tree -Dincludes=com.rabbitmq`
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

# RabbitMQ Java

The amqp-client library is the official RabbitMQ client for the JVM.

## What this skill does

- Configures ConnectionFactory
- Declares queues/exchanges and binds
- Publishes/consumes with callbacks

## When to use

- JVM services on RabbitMQ
- RPC over AMQP

## Real commands

```bash
mvn compile
mvn exec:java -Dexec.mainClass=com.example.Publisher
mvn package
mvn dependency:tree -Dincludes=com.rabbitmq
```

## Publish

```java
ConnectionFactory f = new ConnectionFactory();
f.setUri("amqp://guest:guest@localhost:5672/");
Connection c = f.newConnection();
Channel ch = c.createChannel();
ch.queueDeclare("tasks", true, false, false, null);
ch.basicPublish("", "tasks", null, "job".getBytes());
```

## Consume

```java
channel.basicConsume("tasks", true, (tag, delivery) -> {
    System.out.println(new String(delivery.getBody()));
}, tag -> {});
```

## pom.xml

```xml
<dependency>
  <groupId>com.rabbitmq</groupId>
  <artifactId>amqp-client</artifactId>
  <version>5.20.0</version>
</dependency>
```

## Best practices

- Use one channel per thread
- Set basicQos for fair dispatch
- Close connections on shutdown hooks

## Capabilities

### rabbitmq-java-client
Use amqp-client in Maven projects for queues, exchanges, publishers and consumers.

**Parameters:**
- `main_class` (string): Java main class to run
- `queue` (string): Queue name
- `uri` (string): AMQP URI

**Commands:**
- `mvn dependency:tree -Dincludes=com.rabbitmq`
- `mvn compile`
- `mvn exec:java -Dexec.mainClass=com.example.Publisher`
- `mvn package`
- `rabbitmqctl list_queues name messages`

**Examples:**
- mvn exec:java -Dexec.mainClass=com.example.Consumer
- mvn compile
- rabbitmqctl list_queues name messages

## References
- [RabbitMQ Java API Guide](https://www.rabbitmq.com/clients/java-api-guide.html)
- [amqp-client GitHub](https://github.com/rabbitmq/rabbitmq-java-client)
