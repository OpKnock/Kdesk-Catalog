---
type: agent_requested
description: "Build and run Kafka Streams applications: topology processing, state-store changelogs, application resets, and output topic verification."
---

# Kafka Streams

Build and run Kafka Streams applications: topology processing, state-store changelogs, application resets, and output topic verification.

## Instructions

# Kafka Streams

Build stateful stream-processing apps on top of Kafka.

## What this skill does

- Runs Kafka Streams topologies built with the DSL (map, groupBy, count).
- Manages state-store changelogs and repartition topics.
- Resets applications for replays and verification of outputs.

## When to use

- Real-time aggregations (counts, averages, windows).
- Enrichment/filtering pipelines that stay within Kafka.
- Exactly-once processing semantics with the Streams DSL.

## Real commands

```bash
# Run the app
java -jar build/libs/kafka-streams-demo.jar config/streams.properties
./gradlew run

# List Streams internal topics
kafka-topics.sh --bootstrap-server localhost:9092 --list | grep -E 'changelog|repartition'

# Reset the app (stop it first) to replay from input topics
kafka-streams-application-reset.sh --bootstrap-server localhost:9092 \
  --application-id wordcount-app \
  --input-topics lines \
  --intermediate-topics wordcount-store-changelog

# Force reset when regular reset is blocked
kafka-streams-application-reset.sh --bootstrap-server localhost:9092 \
  --application-id wordcount-app --force

# Verify output (keys + values)
kafka-console-consumer.sh --bootstrap-server localhost:9092 \
  --topic wordcount-output --from-beginning \
  --property print.key=true --property print.value=true

# Group state of the streams app
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --describe --group wordcount-app
```

## Topology example (WordCount)

```java
StreamsBuilder builder = new StreamsBuilder();
KStream<String, String> lines = builder.stream("lines");
lines
  .flatMapValues(line -> Arrays.asList(line.toLowerCase().split(" ")))
  .groupBy((key, word) -> word)
  .count(Materialized.as("wordcount-store"))
  .toStream()
  .to("wordcount-output", Produced.with(Serdes.String(), Serdes.Long()));
```

## streams.properties example

```properties
application.id=wordcount-app
bootstrap.servers=localhost:9092
default.key.serde=org.apache.kafka.common.serialization.Serdes$StringSerde
default.value.serde=org.apache.kafka.common.serialization.Serdes$StringSerde
processing.guarantee=exactly_once_v2
```

## Testing

```bash
# Feed input, watch output
echo 'the quick brown fox' | kafka-console-producer.sh --bootstrap-server localhost:9092 --topic lines
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic wordcount-output --from-beginning --property print.key=true
```

## Best practices

- Set processing.guarantee=exactly_once_v2 for accurate counts.
- Reset the app (not delete topics) for deterministic replays.
- Monitor the streams thread: LAG on changelogs signals state restore in progress.

## Capabilities

### streams-app
Run Kafka Streams applications and manage their lifecycle.

**Commands:**
- `java -jar build/libs/kafka-streams-demo.jar config/streams.properties`
- `./gradlew run`
- `kafka-streams-application-reset.sh --bootstrap-server localhost:9092 --application-id wordcount-app --input-topics lines --intermediate-topics wordcount-store-changelog`
- `kafka-streams-application-reset.sh --bootstrap-server localhost:9092 --application-id wordcount-app --force`

**Examples:**
- java -jar build/libs/kafka-streams-demo.jar config/streams.properties
- kafka-streams-application-reset.sh --bootstrap-server localhost:9092 --application-id wordcount-app --input-topics lines --intermediate-topics wordcount-store-changelog
- ./gradlew run

### output-verify
Verify stream processing output and internal topology state.

**Commands:**
- `kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic wordcount-output --from-beginning --property print.key=true --property print.value=true`
- `kafka-topics.sh --bootstrap-server localhost:9092 --list | grep -E 'wordcount|changelog|repartition'`
- `kafka-streams-application-reset.sh --bootstrap-server localhost:9092 --application-id wordcount-app --list`
- `kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group wordcount-app`

**Examples:**
- kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic wordcount-output --from-beginning --property print.key=true
- kafka-topics.sh --bootstrap-server localhost:9092 --list | grep -E 'changelog|repartition'
- kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group wordcount-app