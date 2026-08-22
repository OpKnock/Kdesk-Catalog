---
name: "nats-client-java"
description: "NATS clients in Java with jnats: Nats.connect, async message handlers, request-reply, and Maven setup."
---

# Nats Client Java

NATS clients in Java with jnats: Nats.connect, async message handlers, request-reply, and Maven setup.

## Instructions

# NATS Java Client

jnats (io.nats:jnats) is the official NATS client for the JVM.

## What this skill does

- Connects with options and connection listeners
- Publishes/subscribes with async message handlers
- Implements request-reply and inbox patterns

## When to use

- Java/Spring services exchanging events over NATS
- High-throughput pub/sub in JVM backends

## Real commands

```bash
mvn compile
mvn exec:java -Dexec.mainClass=com.example.Publisher
mvn package
```

## Publish / subscribe

```java
Connection nc = Nats.connect("nats://localhost:4222");
nc.publish("orders.created", "{\"id\":1}".getBytes(StandardCharsets.UTF_8));
Disposable sub = nc.subscribe("orders.*", msg ->
    System.out.println(new String(msg.getData())));
Thread.sleep(1000);
sub.dispose();
nc.close();
```

## Request-reply

```java
CompletableFuture<Message> reply = nc.request("service.echo", "ping".getBytes());
Message msg = reply.get(2, TimeUnit.SECONDS);
```

## pom.xml

```xml
<dependency>
  <groupId>io.nats</groupId>
  <artifactId>jnats</artifactId>
  <version>2.20.4</version>
</dependency>
```

## Best practices

- Close connections in finally blocks
- Use dispatch listeners for long-lived subscriptions
- Prefer `Nats.connect(Options)` with `maxReconnects` for HA

## Capabilities

### nats-java-client
Use the jnats library in Maven projects for connect, pub/sub and request-reply patterns.

**Commands:**
- `mvn dependency:tree`
- `mvn compile`
- `mvn package`
- `mvn exec:java -Dexec.mainClass=com.example.Publisher`
- `curl -s https://repo1.maven.org/maven2/io/nats/jnats/maven-metadata.xml`

**Examples:**
- mvn exec:java -Dexec.mainClass=com.example.Subscriber
- mvn dependency:tree -Dincludes=io.nats
- mvn test
