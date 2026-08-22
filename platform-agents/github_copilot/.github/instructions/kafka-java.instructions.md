---
applyTo: "**/*.java **/*.r **/*.sh"
---

# Kafka Java

Build Kafka clients in Java with the official kafka-clients library: Maven setup, producer/consumer apps, and end-to-end topic verification.

## Instructions

# Kafka (Java)

Build Kafka producers and consumers with the official kafka-clients library.

## What this skill does

- Scaffolds Maven projects with kafka-clients dependency.
- Runs Java producer/consumer applications.
- Verifies the pipeline end-to-end with the Kafka CLI.

## When to use

- JVM services publishing or consuming events.
- Migrating Spring Boot apps to lean kafka-clients.
- Replacing kafka-console tools with typed applications.

## Real commands

```bash
# Scaffold
mvn archetype:generate \
  -DgroupId=com.mycompany -DartifactId=orders-consumer \
  -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false

# Add kafka-clients to pom.xml
mvn dependency:get -Dartifact=org.apache.kafka:kafka-clients:3.6.0

# Build and run
mvn package
java -jar target/orders-consumer-1.0-SNAPSHOT.jar

# End-to-end verification
kafka-topics.sh --bootstrap-server localhost:9092 --create --topic orders --partitions 3 --replication-factor 1
kafka-console-producer.sh --bootstrap-server localhost:9092 --topic orders
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic orders --from-beginning
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group orders-java
```

## pom.xml dependency

```xml
<dependency>
  <groupId>org.apache.kafka</groupId>
  <artifactId>kafka-clients</artifactId>
  <version>3.6.0</version>
</dependency>
```

## Producer snippet

```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");
Producer<String, String> p = new KafkaProducer<>(props);
p.send(new ProducerRecord<>("orders", "order-1", "{"qty":2}"));
p.close();
```

## Testing

```bash
mvn test
```

## Best practices

- Use a shared KafkaProducer singleton; producers are thread-safe.
- Configure acks=all and enable.idempotence=true for safe writes.
- Set max.poll.records and max.poll.interval.ms so rebalances don't fire.

## Capabilities

### java-client-app
Scaffold and run Java Kafka producer/consumer applications with Maven.

**Commands:**
- `mvn archetype:generate -DgroupId=com.mycompany -DartifactId=orders-consumer -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false`
- `mvn package`
- `java -jar target/orders-consumer-1.0-SNAPSHOT.jar`
- `mvn test`

**Examples:**
- mvn archetype:generate -DgroupId=com.mycompany -DartifactId=orders-consumer -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false
- mvn package && java -jar target/orders-consumer-1.0-SNAPSHOT.jar
- mvn dependency:tree | grep kafka-clients

### end-to-end
Produce and consume test data alongside the Java app for verification.

**Commands:**
- `kafka-topics.sh --bootstrap-server localhost:9092 --create --topic orders --partitions 3 --replication-factor 1`
- `kafka-console-producer.sh --bootstrap-server localhost:9092 --topic orders`
- `kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic orders --from-beginning`
- `kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group orders-java`

**Examples:**
- kafka-topics.sh --bootstrap-server localhost:9092 --create --topic orders --partitions 3 --replication-factor 1
- kafka-console-producer.sh --bootstrap-server localhost:9092 --topic orders
- kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group orders-java
