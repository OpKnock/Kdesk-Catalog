# event-driven-architect-event-driven-architect

Designs event-driven systems on Kafka, RabbitMQ, NATS, and Pulsar: topics, queues, consumers, offsets, and stream operations.

## Instructions

# Event-Driven Architecture

Design and operate event streaming and messaging systems.

## What This Skill Does

- Creates topics and manages partitions/replication
- Produces and consumes events from the CLI
- Inspects consumer group lag and offsets
- Operates RabbitMQ/NATS/Pulsar brokers
- Advises on event contracts and schemas

## When to Use

- Designing a new event flow between services
- Debugging consumer lag or missed events
- Choosing between broker technologies

## Real Commands

```bash
# Kafka
kafka-topics.sh --bootstrap-server localhost:9092 --create   --topic orders --partitions 6 --replication-factor 3
kafka-topics.sh --bootstrap-server localhost:9092 --list
kafka-console-producer.sh --bootstrap-server localhost:9092 --topic orders
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic orders --from-beginning
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group payments

# RabbitMQ
rabbitmqctl status
rabbitmqctl list_queues name messages consumers
rabbitmqctl list_bindings

# NATS
nats pub orders.new '{"id":1}'
nats sub orders.>
nats stream add ORDERS --subjects 'orders.>' --storage file

# Pulsar
pulsar-admin topics list public/default
pulsar-admin topics stats persistent://public/default/orders
```

## Design Rules

- Partition by key for ordering per entity
- Design events as facts: immutable, versioned
- Handle out-of-order and duplicate delivery (idempotency)
- Keep brokers outside the request path
- Schema-register event payloads for compatibility

## Best Practices

- Monitor consumer lag as a core SLO
- Use dead-letter topics for poison messages
- Back-pressure consumers, never unbounded buffers
- Test broker failover with partition leadership moves
- Version topics (orders.v1) for breaking changes

## Capabilities

### kafka-operations
Create topics, produce/consume events, and manage consumer groups.

**Commands:**
- `kafka-topics.sh --bootstrap-server localhost:9092 --create --topic orders --partitions 6 --replication-factor 3`
- `kafka-topics.sh --bootstrap-server localhost:9092 --list`
- `kafka-console-producer.sh --bootstrap-server localhost:9092 --topic orders`
- `kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic orders --from-beginning`
- `kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list`
- `kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group payments`

**Examples:**
- kafka-topics.sh --bootstrap-server localhost:9092 --create --topic orders --partitions 6
- kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic orders --from-beginning
- kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group payments

### brokers-and-streams
Operate RabbitMQ, NATS, and Pulsar brokers.

**Commands:**
- `rabbitmqctl status`
- `rabbitmqctl list_queues name messages consumers`
- `rabbitmqctl list_bindings`
- `nats pub orders.new '{"id":1}'`
- `nats sub orders.>`
- `pulsar-admin topics list public/default`

**Examples:**
- rabbitmqctl list_queues name messages consumers
- nats pub orders.new '{"id":1}'
- pulsar-admin topics list public/default