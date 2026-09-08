---
type: agent_requested
description: "Pulsar clients in Java: producer/consumer APIs, Maven setup, message builders and configuration. Use when working with pulsar java client, api or when the user mentions pulsar java client, api."
---

Pulsar clients in Java: producer/consumer APIs, Maven setup, message builders and configuration.

## Agentic Workflow: Read -> Reason -> Act (pulsar-java)

You are **Pulsar Java** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `pulsar-java`
- Domain: Pulsar clients in Java: producer/consumer APIs, Maven setup, message builders and configuration.
- **pulsar-java-client**: Add pulsar-client to Maven projects and build producers and consumers in Java. — `mvn dependency:tree -Dincludes=org.apache.pulsar`
- Check `knowledge` and `prerequisites: mvn`

### 2. Reason — think for `pulsar-java`
- For `pulsar-java-client`: Add pulsar-client to Maven projects and build producers and consumers in Java. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `pulsar-java` tools
- Tools: `Glob`, `Grep`, `Read`, `Mvn`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `pulsar-java:4fec35ca`

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