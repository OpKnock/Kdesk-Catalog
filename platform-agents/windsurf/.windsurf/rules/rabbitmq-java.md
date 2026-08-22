---
trigger: glob
description: "RabbitMQ clients in Java with amqp-client: ConnectionFactory, publishes, consumers, and RPC patterns."
globs: ["**/*.java", "**/*.r", "**/*.sh"]
---

# Rabbitmq Java

RabbitMQ clients in Java with amqp-client: ConnectionFactory, publishes, consumers, and RPC patterns.

## Instructions

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
