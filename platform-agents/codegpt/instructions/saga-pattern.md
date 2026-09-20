# Saga Pattern

Expert saga pattern skill covering choreographed and orchestrated sagas with Temporal CLI, workflow inspection, compensation design, and failure injection.

## Instructions

# Saga Pattern

Expert skill for distributed transactions using the saga pattern.

## What this skill does

- Breaks a distributed transaction into local steps with compensations
- Orchestrates steps with Temporal workflows and worker task queues
- Inspects and terminates sagas with the Temporal CLI

## When to use

- An operation spans services (order, payment, inventory, shipping)
- Distributed 2PC is not viable and eventual consistency is acceptable
- You need retries, timeouts, and audit trails for the transaction

## Real commands

```bash
# Local Temporal server for development
temporal server start-dev

# Start a saga workflow
temporal workflow start --workflow-id order-42 --type OrderSaga --task-queue orders

# Inspect progress and history
temporal workflow show --workflow-id order-42
temporal workflow describe --workflow-id order-42

# Clean up a stuck saga
temporal workflow terminate --workflow-id order-42 --reason 'manual cleanup'

# If running Temporal in k8s
kubectl get pods -n temporal
```

## Saga sketch (Go)

```go
func OrderSaga(ctx workflow.Context, o Order) error {
    if err := workflow.ExecuteActivity(ctx, ReservePayment, o).Get(ctx, nil); err != nil {
        return err
    }
    if err := workflow.ExecuteActivity(ctx, ReserveInventory, o).Get(ctx, nil); err != nil {
        workflow.ExecuteActivity(ctx, CancelPayment, o) // compensation
        return err
    }
    return workflow.ExecuteActivity(ctx, ConfirmOrder, o).Get(ctx, nil)
}
```

## Failure testing

```bash
temporal workflow start --workflow-id order-43 --type OrderSaga --task-queue orders
temporal workflow terminate --workflow-id order-43 --reason 'fail'
temporal workflow show --workflow-id order-43   # verify compensation ran
```

## Best practices

- Write a compensation for every step that reserves or mutates state
- Make compensations idempotent; they may run twice
- Prefer orchestrated sagas when steps change often

## Capabilities

### temporal-saga
Model distributed transactions as sagas and drive them with Temporal

**Commands:**
- `temporal server start-dev`
- `temporal workflow start --workflow-id order-42 --type OrderSaga --task-queue orders`
- `temporal workflow show --workflow-id order-42`
- `temporal workflow terminate --workflow-id order-42 --reason 'manual cleanup'`
- `kubectl get pods -n temporal`

**Examples:**
- temporal workflow start --workflow-id order-42 --type OrderSaga --task-queue orders
- temporal workflow show --workflow-id order-42
- temporal workflow describe --workflow-id order-42
