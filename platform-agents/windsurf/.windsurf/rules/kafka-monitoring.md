---
trigger: glob
description: "Monitor Kafka brokers and clients: JMX metrics with JmxTool, broker API versions, log dir health, and JMX-to-Prometheus exporter setup."
globs: ["**/*.go", "**/*.java", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

# Kafka Monitoring

Monitor Kafka brokers and clients: JMX metrics with JmxTool, broker API versions, log dir health, and JMX-to-Prometheus exporter setup.

## Instructions

# Kafka Monitoring

Monitor Kafka brokers and client metrics with the Kafka CLI and JMX tooling.

## What this skill does

- Checks broker API versions and log directory health.
- Samples broker JMX metrics with kafka.tools.JmxTool.
- Bootstraps the JMX-to-Prometheus exporter for dashboards.

## When to use

- Capacity planning (BytesInPerSec, BytesOutPerSec).
- Debugging disk and network saturation on brokers.
- Verifying a fresh cluster is healthy before go-live.

## Real commands

```bash
# Broker API versions (also shows broker->client compatibility)
kafka-broker-api-versions.sh --bootstrap-server localhost:9092

# Log dir health (disk errors, sizes)
kafka-log-dirs.sh --bootstrap-server localhost:9092 --describe --broker-list 1

# Partitions with unclean leader elections
kafka-topics.sh --bootstrap-server localhost:9092 --describe --unclean-offset-leader-available

# Sample a metric every 5s from JMX
kafka-run-class.sh kafka.tools.JmxTool \
  --object-name kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec \
  --reporting-interval 5000 \
  --jmx-url service:jmx:rmi:///jndi/rmi://localhost:9999/jmxrmi

# Request handler pool utilization
kafka-run-class.sh kafka.tools.JmxTool \
  --object-name kafka.server:type=KafkaRequestHandlerPool,name=RequestHandlerAvgIdlePercent

# Prometheus exporter on broker start
java -javaagent:jmx_prometheus_javaagent.jar=7071:config.yaml \
  -jar kafka-server.jar config/server.properties

# Verify exporter is serving
curl -s localhost:7071/metrics | grep BytesInPerSec
```

## Prometheus config.yaml example

```yaml
lowercaseOutputName: true
rules:
  - pattern: kafka.server<type=BrokerTopicMetrics, name=(.*)><>(Value)
    name: kafka_broker_topic_$1
    type: GAUGE
```

## Testing

```bash
# Produce traffic then watch BytesInPerSec climb
kafka-console-producer.sh --bootstrap-server localhost:9092 --topic test
```

## Best practices

- Enable JMX on brokers (-Dcom.sun.management.jmxremote.port=9999).
- Scrape request handler idle %, ISR shrink rate, and under-replicated partitions.
- Use the kafka.server:type=KafkaServer,name=BrokerState metric for broker liveness.

## Capabilities

### broker-health
Query broker health, API versions, and log directories.

**Commands:**
- `kafka-broker-api-versions.sh --bootstrap-server localhost:9092`
- `kafka-log-dirs.sh --bootstrap-server localhost:9092 --describe --broker-list 1`
- `kafka-topics.sh --bootstrap-server localhost:9092 --describe --unclean-offset-leader-available`
- `kafka-broker-api-versions.sh --bootstrap-server localhost:9092 --version`

**Examples:**
- kafka-broker-api-versions.sh --bootstrap-server localhost:9092
- kafka-log-dirs.sh --bootstrap-server localhost:9092 --describe --broker-list 1 | jq '.brokers[].logDirs[].errorCode'
- kafka-topics.sh --bootstrap-server localhost:9092 --describe --unclean-offset-leader-available

### jmx-metrics
Pull broker JMX metrics with kafka.tools.JmxTool and export to Prometheus.

**Commands:**
- `kafka-run-class.sh kafka.tools.JmxTool --object-name kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec --date-format 'yyyy-MM-dd HH:mm:ss' --jmx-url service:jmx:rmi:///jndi/rmi://localhost:9999/jmxrmi`
- `kafka-run-class.sh kafka.tools.JmxTool --object-name kafka.server:type=KafkaRequestHandlerPool,name=RequestHandlerAvgIdlePercent --reporting-interval 10000`
- `java -javaagent:jmx_prometheus_javaagent.jar=7071:config.yaml -jar kafka-server.jar config/server.properties`

**Examples:**
- kafka-run-class.sh kafka.tools.JmxTool --object-name kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec --date-format 'yyyy-MM-dd HH:mm:ss' --jmx-url service:jmx:rmi:///jndi/rmi://localhost:9999/jmxrmi
- java -javaagent:jmx_prometheus_javaagent.jar=7071:config.yaml -jar kafka-server.jar config/server.properties
- curl -s localhost:7071/metrics | grep BytesInPerSec
