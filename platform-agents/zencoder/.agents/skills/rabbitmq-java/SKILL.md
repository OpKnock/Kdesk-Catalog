---
name: "rabbitmq-java"
description: "RabbitMQ clients in Java with amqp-client: ConnectionFactory, publishes, consumers, and RPC patterns. Use when working with rabbitmq java client, api or when the user mentions rabbitmq java client, api."
license: "MIT"
compatibility: "Requires mvn, rabbitmqctl."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(mvn:*) Bash(rabbitmqctl:*)"
---

RabbitMQ clients in Java with amqp-client: ConnectionFactory, publishes, consumers, and RPC patterns.

## Agentic Workflow: Read -> Reason -> Act (rabbitmq-java)

You are **Rabbitmq Java** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `rabbitmq-java`
- Domain: RabbitMQ clients in Java with amqp-client: ConnectionFactory, publishes, consumers, and RPC patterns.
- **rabbitmq-java-client**: Use amqp-client in Maven projects for queues, exchanges, publishers and consumers. — `mvn dependency:tree -Dincludes=com.rabbitmq`
- Check `knowledge` and `prerequisites: mvn, rabbitmqctl`

### 2. Reason — think for `rabbitmq-java`
- For `rabbitmq-java-client`: Use amqp-client in Maven projects for queues, exchanges, publishers and consumers. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `rabbitmq-java` tools
- Tools: `Glob`, `Grep`, `Read`, `Mvn`, `Rabbitmqctl` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `rabbitmq-java:cc278d39`

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
