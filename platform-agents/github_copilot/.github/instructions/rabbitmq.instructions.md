---
applyTo: "**/*.json **/*.r **/*.sh"
---

# Rabbitmq

Operates RabbitMQ brokers: vhosts, users, queues, exchanges, and message flow with rabbitmqctl and rabbitmqadmin.

## Instructions

# RabbitMQ

Operate RabbitMQ with the official admin tools.

## When to Use

- Work queues and routing topologies
- Managing vhosts/users for multi-team isolation
- DLQ and TTL design

## Broker status

```bash
rabbitmqctl status
rabbitmqctl list_queues name messages consumers --formatter table
```

## Multi-tenancy

```bash
rabbitmqctl add_vhost orders_vhost
rabbitmqctl add_user svc_orders secret123
rabbitmqctl set_permissions -p orders_vhost svc_orders '.*' '.*' '.*'
```

Use separate vhosts per team/environment.

## Topology via rabbitmqadmin

```bash
rabbitmqadmin declare exchange name=order.events type=topic durable=true
rabbitmqadmin declare queue name=orders durable=true
rabbitmqadmin declare binding source=order.events destination=orders routing_key='orders.*'
```

## Consuming for debugging

```bash
rabbitmqadmin get queue=orders count=10 ackmode=ack_requeue_true --format=json
```

## DLQ pattern

Declare `dead.orders` with the same type, bind via DLX args:

```bash
rabbitmqadmin declare queue name=orders durable=true arguments='{"x-dead-letter-exchange":"order.dlx","x-message-ttl":30000}'
```

## Best practices

- Durable queues + persistent messages for critical flows.
- Set prefetch to match consumer CPU profile.
- Watch `messages_unacknowledged` for stuck consumers.
- Rotate user credentials quarterly; least-privilege per vhost.

## Testing

Publish 1k messages to a topic exchange and verify binding fan-out with rabbitmqadmin get.

## Capabilities

### rabbitmqctl
Administer the broker with rabbitmqctl.

**Commands:**
- `rabbitmqctl status`
- `rabbitmqctl list_queues name messages consumers --formatter table`
- `rabbitmqctl add_vhost orders_vhost`
- `rabbitmqctl add_user svc_orders secret123`
- `rabbitmqctl set_permissions -p orders_vhost svc_orders '.*' '.*' '.*'`

**Examples:**
- rabbitmqctl list_queues name messages | sort -k2 -rn | head
- rabbitmqctl list_exchanges name type --formatter json
- rabbitmqctl set_user_tags svc_orders monitoring

### rabbitmqadmin
Declare and inspect topology with rabbitmqadmin.

**Commands:**
- `rabbitmqadmin declare queue name=orders durable=true`
- `rabbitmqadmin declare exchange name=order.events type=topic durable=true`
- `rabbitmqadmin declare binding source=order.events destination=orders routing_key='orders.*'`
- `rabbitmqadmin list queues name messages rate`
- `rabbitmqadmin get queue=orders count=10 --format=json`

**Examples:**
- rabbitmqadmin declare queue name=dead.orders durable=true --vhost=orders_vhost
- rabbitmqadmin list bindings source destination routing_key
- rabbitmqadmin get queue=orders ackmode=ack_requeue_true count=1 --format=raw_json
