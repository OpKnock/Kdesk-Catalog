---
name: "pulsar-java"
description: "Pulsar clients in Java: producer/consumer APIs, Maven setup, message builders and configuration. Use when working with pulsar java client, api or when the user mentions pulsar java client, api."
---

Pulsar clients in Java: producer/consumer APIs, Maven setup, message builders and configuration.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `mvn dependency:tree -Dincludes=org.apache.pulsar`
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

# Pulsar Java

Build Pulsar producers and consumers in Java with the official client library.

## What this skill does

- Configures the Maven dependency
- Writes producer/consumer code
- Uses typed schemas

## When to use

- JVM services in the Pulsar ecosystem
- Replacing Kafka clients with Pulsar

## Real commands

```bash
mvn compile
mvn exec:java -Dexec.mainClass=com.example.Producer
mvn dependency:tree -Dincludes=org.apache.pulsar
mvn package
```

## Producer

```java
PulsarClient client = PulsarClient.builder().serviceUrl("pulsar://localhost:6650").build();
Producer<String> producer = client.newProducer(Schema.STRING)
    .topic("my-topic").create();
producer.send("hello");
client.close();
```

## Consumer

```java
Consumer<String> consumer = client.newConsumer(Schema.STRING)
    .topic("my-topic").subscriptionName("worker").subscribe();
Message<String> msg = consumer.receive();
System.out.println(msg.getValue());
consumer.acknowledge(msg);
```

## pom.xml

```xml
<dependency>
  <groupId>org.apache.pulsar</groupId>
  <artifactId>pulsar-client</artifactId>
  <version>3.2.0</version>
</dependency>
```

## Best practices

- Use schemas (Schema.STRING/JSON) instead of raw bytes
- Always acknowledge received messages
- Tune batching for producer throughput

## Capabilities

### pulsar-java-client
Add pulsar-client to Maven projects and build producers and consumers in Java.

**Parameters:**
- `main_class` (string): Java main class to run
- `topic` (string): Topic name
- `service_url` (string): Pulsar broker URL

**Commands:**
- `mvn dependency:tree -Dincludes=org.apache.pulsar`
- `mvn compile`
- `mvn package`
- `mvn exec:java -Dexec.mainClass=com.example.Producer`
- `curl -s https://repo1.maven.org/maven2/org/apache/pulsar/pulsar-client/maven-metadata.xml`

**Examples:**
- mvn exec:java -Dexec.mainClass=com.example.Consumer
- mvn compile
- mvn dependency:tree -Dincludes=org.apache.pulsar | grep pulsar-client

## References
- [Pulsar Java client docs](https://pulsar.apache.org/docs/3.0.x/client-libraries-java/)
- [pulsar-client on Maven](https://central.sonatype.com/artifact/org.apache.pulsar/pulsar-client)
