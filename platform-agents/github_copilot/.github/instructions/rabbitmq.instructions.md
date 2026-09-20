---
applyTo: "**/*.json **/*.r **/*.sh"
---

Operates RabbitMQ brokers: vhosts, users, queues, exchanges, and message flow with rabbitmqctl and rabbitmqadmin.

## Agentic Workflow: Read -> Reason -> Act (rabbitmq)

You are **Rabbitmq** (messaging/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — messaging context for `rabbitmq`
- Domain: Operates RabbitMQ brokers: vhosts, users, queues, exchanges, and message flow with rabbitmqctl and rabbitmqadmin.
- **rabbitmqctl**: Administer the broker with rabbitmqctl. — `rabbitmqctl status`
- **rabbitmqadmin**: Declare and inspect topology with rabbitmqadmin. — `rabbitmqadmin declare queue name=orders durable=true`
- Check `knowledge` and `prerequisites: rabbitmqadmin, rabbitmqctl`

### 2. Reason — think for `rabbitmq`
- For `rabbitmqctl`: Administer the broker with rabbitmqctl. — decide which checks to run
- For `rabbitmqadmin`: Declare and inspect topology with rabbitmqadmin. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `rabbitmq` tools
- Tools: `Glob`, `Grep`, `Read`, `Rabbitmqctl`, `Rabbitmqadmin` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `rabbitmq:fdc20d3e`

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

**Parameters:**
- `vhost` (string): Virtual host name
- `user` (string): RabbitMQ user
- `formatter` (string): table, tsv, or json

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

**Parameters:**
- `queue` (string): Queue name
- `exchange` (string): Exchange name
- `routing_key` (string): Binding routing key

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

## References
- [RabbitMQ CLI](https://www.rabbitmq.com/docs/cli)
- [RabbitMQ Exchanges](https://www.rabbitmq.com/docs/exchanges)
- [RabbitMQ Queue Guide](https://www.rabbitmq.com/docs/queues)
